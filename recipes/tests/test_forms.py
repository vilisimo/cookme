"""
Test suite for custom form functionality.
"""

from string import capwords

from django.test import TestCase
from django.forms import formset_factory
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User

from ingredients.models import Ingredient, Unit
from recipes.models import Recipe
from recipes.forms import (
    BaseRecipeIngredientFormSet,
    RecipeIngredientForm,
    AddRecipeForm,
)


class AddRecipeFormTests(TestCase):
    """ Test suite to test the AddRecipeForm. """

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')

    def test_add_recipe_form_valid(self):
        """ Ensure that information is entered into the fields. """

        data = {'author': self.user, 'title': 'test', 'description': 'test',
                'cuisine': 'ot', 'steps': 'step'}
        form = AddRecipeForm(data=data)

        self.assertTrue(form.is_valid())

    def test_add_recipe_form_missing_values(self):
        """ Ensure that empty data cannot be passed. """

        data = {'title': '   ', 'description': 'test'}
        form = AddRecipeForm(data=data)

        self.assertFalse(form.is_valid())

        data = {'title': 'test', 'description': ' '}
        form = AddRecipeForm(data=data)

        self.assertFalse(form.is_valid())

        data = {'title': 'test', 'description': 'test', 'cuisine': '  ',
                'steps': 'step'}
        form = AddRecipeForm(data=data)

        self.assertFalse(form.is_valid())

        data = {'title': 'test', 'description': 'test', 'cuisine': 'test',
                'steps': '  '}
        form = AddRecipeForm(data=data)

        self.assertFalse(form.is_valid())

    def test_image_field(self):
        """ Ensure that the form can take image field. """

        with open('static/test/test.png', 'rb') as image:
            data = {'title': 'test', 'description': 'testing', 'cuisine': 'ot',
                    'steps': 'step'}
            image_data = {'image': SimpleUploadedFile(image.name, image.read())}
            form = AddRecipeForm(data=data, files=image_data)

            self.assertTrue(form.is_valid())


class RecipeIngredientFormSetTests(TestCase):
    """ Test suite to ensure that custom formset functions work properly. """

    def setUp(self):
        self.potato = Ingredient.objects.create(name='Potato', type='Vegetable')
        self.tomato = Ingredient.objects.create(name='Tomato', type='Fruit')
        self.unit = Unit.objects.create(name='kilogram', abbrev='kg')
        self.rec_formset = formset_factory(RecipeIngredientForm,
                                           formset=BaseRecipeIngredientFormSet)

    def test_formset_empty(self):
        """
        Ensure that a formset cannot be empty (by default it can, even if all
        fields are required).
        """

        data = {
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '',
        }

        formset = self.rec_formset(data)
        self.assertFalse(formset.is_valid())

    def test_formset_same_ingredients(self):
        """
        Ensure that an error is shown when the same ingredients are typed in.
        """

        data = {
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '',
            'form-0-ingredient': 'test',
            'form-0-unit': str(self.unit.pk),
            'form-0-quantity': '1',
            'form-1-ingredient': 'test',
            'form-1-unit': str(self.unit.pk),
            'form-1-quantity': '1',
        }

        formset = self.rec_formset(data)
        self.assertFalse(formset.is_valid())
        self.assertIn('Ingredients should be distinct.',
                      formset.non_form_errors())

    def test_formset_different_ingredients(self):
        """ Ensure that a user can select different ingredients. """

        data = {
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '',
            'form-0-ingredient': 'test',
            'form-0-unit': str(self.unit.pk),
            'form-0-quantity': '1',
            'form-1-ingredient': 'test2',
            'form-1-unit': str(self.unit.pk),
            'form-1-quantity': '1',
        }

        formset = self.rec_formset(data)
        self.assertTrue(formset.is_valid())


class RecipeIngredientFormTests(TestCase):
    """ Test suite to ensure that RecipeIngredient creation form is ok. """

    def setUp(self):
        self.user = User.objects.create_user(username='test')
        self.unit = Unit.objects.create(name='kilogram', abbrev='kg')
        self.recipe = Recipe.objects.create(author=self.user, title='test',
                                            description='test', steps='test',
                                            cuisine='ot')

    def test_fields_empty(self):
        """ Ensure that information is entered into the fields. """

        data = dict()
        form = RecipeIngredientForm(data=data)

        self.assertFalse(form.is_valid())

        data['ingredient'] = 'test'
        form = RecipeIngredientForm(data=data)

        self.assertFalse(form.is_valid())

        data['unit'] = self.unit.pk
        form = RecipeIngredientForm(data=data)

        self.assertFalse(form.is_valid())

    def test_fields_filled_in(self):
        """ Ensures that filled in form is considered to be valid. """

        data = {'ingredient': 'test', 'unit': self.unit.pk, 'quantity': 1.0}
        form = RecipeIngredientForm(data=data)

        self.assertTrue(form.is_valid(), "Correct data threw an error.")

    def test_fields_valid_create_ingredient_entry(self):
        """
        Ensures that when the form is filled in properly, an Ingredient
        entry is created in the database.

        Note: name is capitalized, since save method capitalizes all words in
        ingredient title.
        """

        name = 'Test'
        data = {'ingredient': name, 'unit': self.unit.pk, 'quantity': 1.0}
        form = RecipeIngredientForm(data=data)

        self.assertTrue(form.is_valid())

        instance = form.save(commit=False)
        instance.recipe = self.recipe
        ingredient = Ingredient.objects.get(name=name)

        self.assertTrue(ingredient)

    def test_fields_ingredient_entry_capitalized(self):
        """
        Ensures that title is correctly capitalized by searching for ingredient
        with capitalized title.
        """

        name = 'test test test'
        data = {'ingredient': name, 'unit': self.unit.pk, 'quantity': 1.0}
        form = RecipeIngredientForm(data=data)

        self.assertTrue(form.is_valid())

        instance = form.save(commit=False)
        instance.recipe = self.recipe
        ingredient = Ingredient.objects.get(name=capwords(name))

        self.assertTrue(ingredient)

    def test_quantity_negative(self):
        """ Ensures that quantity of an ingredient is always positive. """

        data = {'ingredient': 'test', 'unit': self.unit.pk, 'quantity': -0.01}
        form = RecipeIngredientForm(data=data)

        self.assertFalse(form.is_valid())

    def test_fields_non_existent_pks(self):
        """
        Ensures that an error is thrown if non-existent PKs are selected.
        Should not be possible to do - but good to check nevertheless.
        """

        data = {'ingredient': 'test', 'unit': 9999, 'quantity': 1}
        form = RecipeIngredientForm(data=data)

        self.assertFalse(form.is_valid())

    def test_negative_value(self):
        """ Ensure that negative value for quantity is not allowed. """

        data = {'ingredient': 'test', 'unit': self.unit.pk, 'quantity': -0.1}
        form = RecipeIngredientForm(data=data)

        self.assertFalse(form.is_valid(), "Negative value was allowed.")
