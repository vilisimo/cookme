from string import capwords

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.forms import formset_factory
from django.test import TestCase

from ingredients.models import Ingredient, Unit
from recipes.forms import (
    BaseRecipeIngredientFormSet as BaseFormSet,
    RecipeIngredientForm,
    AddRecipeForm,
)
from recipes.models import Recipe


class AddRecipeFormTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='test', password='test')
        self.data = {
            'author': user,
            'title': 'test',
            'description': 'test',
            'cuisine': 'ot',
            'steps': 'step'
        }

    def test_add_recipe_form_valid_data(self):
        form = AddRecipeForm(data=self.data)

        self.assertTrue(form.is_valid())

    def test_add_recipe_form_missing_title_not_allowed(self):
        self.data['title'] = '   '

        form = AddRecipeForm(data=self.data)

        self.assertFalse(form.is_valid())

    def test_add_recipe_form_missing_description_not_allowed(self):
        self.data['description'] = ' '

        form = AddRecipeForm(data=self.data)

        self.assertFalse(form.is_valid())

    def test_add_recipe_form_missing_cuisine_not_allowed(self):
        self.data['cuisine'] = '  '

        form = AddRecipeForm(data=self.data)

        self.assertFalse(form.is_valid())

    def test_add_recipe_form_missing_steps_not_allowed(self):
        self.data['steps'] = '  '

        form = AddRecipeForm(data=self.data)

        self.assertFalse(form.is_valid())

    def test_image_field(self):
        with open('static/test/test.png', 'rb') as image:
            image_data = {'image': SimpleUploadedFile(image.name, image.read())}

            form = AddRecipeForm(data=self.data, files=image_data)

            self.assertTrue(form.is_valid())


class RecipeIngredientFormSetTests(TestCase):
    def setUp(self):
        unit = Unit.objects.create(name='kilogram', abbrev='kg')
        self.rec_formset = formset_factory(RecipeIngredientForm, formset=BaseFormSet)
        self.data = {
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '',
            'form-0-ingredient': 'test',
            'form-0-unit': str(unit.pk),
            'form-0-quantity': '1',
            'form-1-ingredient': 'test2',
            'form-1-unit': str(unit.pk),
            'form-1-quantity': '1',
        }

    def test_formset_empty_not_allowed(self):
        """ By default it can be empty, even if all fields are required. """

        data = {
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '',
        }

        formset = self.rec_formset(data)

        self.assertFalse(formset.is_valid())

    def test_formset_same_ingredients_not_allowed(self):
        self.data['form-1-ingredient'] = 'test'
        expected_error = 'Ingredients should be distinct.'

        formset = self.rec_formset(self.data)

        self.assertFalse(formset.is_valid())
        self.assertIn(expected_error, formset.non_form_errors())

    def test_formset_different_ingredients_allowed(self):
        formset = self.rec_formset(self.data)

        self.assertTrue(formset.is_valid())


class RecipeIngredientFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test')
        self.unit = Unit.objects.create(name='kilogram', abbrev='kg')
        self.recipe = Recipe.objects.create(author=self.user, title='test', description='test',
                                            steps='test', cuisine='ot')
        self.data = {
            'ingredient': 'test',
            'unit': self.unit.pk,
            'quantity': 1.0
        }

    def test_empty_fields_not_allowed(self):
        form = RecipeIngredientForm(data=(dict()))

        self.assertFalse(form.is_valid())

    def test_missing_unit_field_not_allowed(self):
        self.data['unit'] = ' '

        form = RecipeIngredientForm(data=self.data)

        self.assertFalse(form.is_valid())

    def test_missing_quantity_field_not_allowed(self):
        self.data['quantity'] = None

        form = RecipeIngredientForm(data=self.data)

        self.assertFalse(form.is_valid())

    def test_filled_in_fields_valid(self):
        form = RecipeIngredientForm(data=self.data)

        self.assertTrue(form.is_valid(), 'Correct data threw an error.')

    def test_valid_fields_create_ingredient_entry(self):
        """
        Note: 'name' variable is capitalized, since save method capitalizes all
        words in ingredient title.
        """

        form = RecipeIngredientForm(data=self.data)
        self.assertTrue(form.is_valid())

        instance = form.save(commit=False)
        instance.recipe = self.recipe
        ingredient = Ingredient.objects.get(name='Test')

        self.assertTrue(ingredient)

    def test_ingredient_entry_capitalized_upon_save(self):
        name = 'test test test'
        self.data['ingredient'] = name
        form = RecipeIngredientForm(data=self.data)

        self.assertTrue(form.is_valid())

        instance = form.save(commit=False)
        instance.recipe = self.recipe
        ingredient = Ingredient.objects.get(name=capwords(name))

        self.assertTrue(ingredient)

    def test_negative_quantity_not_allowed(self):
        self.data['quantity'] = -0.01

        form = RecipeIngredientForm(data=self.data)

        self.assertFalse(form.is_valid())

    def test_non_existent_pks_not_allowed(self):
        self.data['unit'] = 9999

        form = RecipeIngredientForm(data=self.data)

        self.assertFalse(form.is_valid())
