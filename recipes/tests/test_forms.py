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
    """
    Test suite to test the AddRecipeForm and ensure that it does not accept
    invalid input.
    """

    def setUp(self):
        user = User.objects.create_user(username='test', password='test')
        self.data = {
            'author': user,
            'title': 'test',
            'description': 'test',
            'cuisine': 'ot',
            'steps': 'step'
        }

    def test_add_recipe_form_valid(self):
        """ Ensures that information is entered into the fields. """

        form = AddRecipeForm(data=self.data)

        self.assertTrue(form.is_valid())

    def test_add_recipe_form_missing_title(self):
        """ Ensures that empty title cannot be passed. """

        self.data['title'] = '   '
        form = AddRecipeForm(data=self.data)

        self.assertFalse(form.is_valid())

    def test_add_recipe_form_missing_description(self):
        """ Ensures that empty description cannot be passed. """

        self.data['description'] = ' '
        form = AddRecipeForm(data=self.data)

        self.assertFalse(form.is_valid())

    def test_add_recipe_form_missing_cuisine(self):
        """ Ensures that empty cuisine field cannot be passed. """

        self.data['cuisine'] = '  '
        form = AddRecipeForm(data=self.data)

        self.assertFalse(form.is_valid())

    def test_add_recipe_form_missing_steps(self):
        """ Ensures that empty steps field cannot be passed. """
        self.data['steps'] = '  '
        form = AddRecipeForm(data=self.data)

        self.assertFalse(form.is_valid())

    def test_image_field(self):
        """ Ensures that the form can take image field. """

        with open('static/test/test.png', 'rb') as image:
            image_data = {'image': SimpleUploadedFile(image.name, image.read())}
            form = AddRecipeForm(data=self.data, files=image_data)

            self.assertTrue(form.is_valid())


class RecipeIngredientFormSetTests(TestCase):
    """ Test suite to ensure that custom formset functions work properly. """

    def setUp(self):
        unit = Unit.objects.create(name='kilogram', abbrev='kg')
        self.rec_formset = formset_factory(RecipeIngredientForm,
                                           formset=BaseRecipeIngredientFormSet)
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

    def test_formset_empty(self):
        """
        Ensures that a formset cannot be empty (by default it can, even if all
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
        Ensures that an error is shown when the same ingredients are typed in.
        """

        self.data['form-1-ingredient'] = 'test'
        formset = self.rec_formset(self.data)
        expected_error = 'Ingredients should be distinct.'

        self.assertFalse(formset.is_valid())
        self.assertIn(expected_error, formset.non_form_errors())

    def test_formset_different_ingredients(self):
        """ Ensures that a user can select different ingredients. """

        formset = self.rec_formset(self.data)

        self.assertTrue(formset.is_valid())


class RecipeIngredientFormTests(TestCase):
    """
    Test suite to ensure that RecipeIngredient creation form validates input
    and throws correct errors.
    """

    def setUp(self):
        self.user = User.objects.create_user(username='test')
        self.unit = Unit.objects.create(name='kilogram', abbrev='kg')
        self.recipe = Recipe.objects.create(author=self.user, title='test',
                                            description='test', steps='test',
                                            cuisine='ot')
        self.data = {
            'ingredient': 'test',
            'unit': self.unit.pk,
            'quantity': 1.0
        }

    def test_fields_empty(self):
        """ Ensures that information is entered into the fields. """

        data = dict()
        form = RecipeIngredientForm(data=data)

        self.assertFalse(form.is_valid())

    def test_field_missing_unit(self):
        """ Ensures that an empty unit field is not allowed. """

        self.data['unit'] = ' '
        form = RecipeIngredientForm(data=self.data)

        self.assertFalse(form.is_valid())

    def test_field_missing_quantity(self):
        """ Ensures that an empty quantity field is not allowed. """

        self.data['quantity'] = None
        form = RecipeIngredientForm(data=self.data)

        self.assertFalse(form.is_valid())

    def test_fields_filled_in(self):
        """ Ensures that filled in form is considered to be valid. """

        form = RecipeIngredientForm(data=self.data)

        self.assertTrue(form.is_valid(), 'Correct data threw an error.')

    def test_fields_valid_create_ingredient_entry(self):
        """
        Ensures that when the form is filled in properly, an Ingredient
        entry is created in the database.

        Note: 'name' variable is capitalized, since save method capitalizes all
        words in ingredient title.
        """

        name = 'Test'
        form = RecipeIngredientForm(data=self.data)

        # Ensures that the form is valid before submitting it.
        self.assertTrue(form.is_valid())

        instance = form.save(commit=False)
        instance.recipe = self.recipe
        ingredient = Ingredient.objects.get(name=name)

        # Now checks that ingredient was truly created.
        self.assertTrue(ingredient)

    def test_fields_ingredient_entry_capitalized(self):
        """
        Ensures that title is correctly capitalized by searching for ingredient
        with capitalized title.
        """

        name = 'test test test'
        self.data['ingredient'] = name
        form = RecipeIngredientForm(data=self.data)

        self.assertTrue(form.is_valid())

        instance = form.save(commit=False)
        instance.recipe = self.recipe
        ingredient = Ingredient.objects.get(name=capwords(name))

        self.assertTrue(ingredient)

    def test_quantity_negative(self):
        """ Ensures that quantity of an ingredient is always positive. """

        self.data['quantity'] = -0.01
        form = RecipeIngredientForm(data=self.data)

        self.assertFalse(form.is_valid())

    def test_fields_non_existent_pks(self):
        """
        Ensures that an error is thrown if non-existent PKs are selected.
        Should not be possible to do - but good to check nevertheless.
        """

        self.data['unit'] = 9999
        form = RecipeIngredientForm(data=self.data)

        self.assertFalse(form.is_valid())
