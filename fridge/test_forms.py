"""
Test suite for custom form functionality.
"""


from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from django.forms import formset_factory
from django.test import TestCase

from ingredients.models import Ingredient, Unit
from .forms import AddRecipeFridgeForm, RecipeIngredientForm
from .forms import BaseRecipeIngredientFormSet


class RecipeIngredientFormSetTests(TestCase):
    """ Test suite to ensure that custom formset functions work properly """

    def setUp(self):
        self.potato = Ingredient.objects.create(name='Potato', type='Vegetable')
        self.tomato = Ingredient.objects.create(name='Tomato', type='Fruit')
        self.unit = Unit.objects.create(name='kilogram', abbrev='kg')

    def test_formset_empty(self):
        """
        Ensure that a formset cannot be empty (by default it can, even if all
        fields are required)
        """

        RecInFormSet = formset_factory(RecipeIngredientForm,
                                       formset=BaseRecipeIngredientFormSet)
        data = {
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '',
        }

        formset = RecInFormSet(data)
        self.assertFalse(formset.is_valid())

    def test_formset_same_ingredients(self):
        """
        Ensure that an error is shown when the same ingredients are selected
        """

        RecInFormSet = formset_factory(RecipeIngredientForm,
                                       formset=BaseRecipeIngredientFormSet)

        data = {
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '',
            'form-0-ingredient': str(self.potato.pk),  # is str needed?
            'form-0-unit': str(self.unit.pk),  # same?
            'form-0-quantity': '1',
            'form-1-ingredient': str(self.potato.pk),  # is str needed?
            'form-1-unit': str(self.unit.pk),  # same?
            'form-1-quantity': '1',
        }

        formset = RecInFormSet(data)
        self.assertFalse(formset.is_valid())
        self.assertIn('Ingredients should be distinct.',
                      formset.non_form_errors())

    def test_formset_different_ingredients(self):
        """ Ensure that a user can select different ingredients """

        RecInFormSet = formset_factory(RecipeIngredientForm,
                                       formset=BaseRecipeIngredientFormSet)

        data = {
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '',
            'form-0-ingredient': str(self.potato.pk),
            'form-0-unit': str(self.unit.pk),
            'form-0-quantity': '1',
            'form-1-ingredient': str(self.tomato.pk),
            'form-1-unit': str(self.unit.pk),
            'form-1-quantity': '1',
        }

        formset = RecInFormSet(data)
        self.assertTrue(formset.is_valid())


class RecipeIngredientFormTests(TestCase):
    """ Test suite to ensure that RecipeIngredient creation form is ok """

    def setUp(self):
        self.potato = Ingredient.objects.create(name='Potato', type='Vegetable')
        self.tomato = Ingredient.objects.create(name='Tomato', type='Fruit')
        self.unit = Unit.objects.create(name='kilogram', abbrev='kg')

    def test_fields_empty(self):
        """ Ensure that information is entered into the fields """

        data = dict()
        form = RecipeIngredientForm(data=data)

        self.assertFalse(form.is_valid())

        data['ingredient'] = self.potato.pk
        form = RecipeIngredientForm(data=data)
        self.assertFalse(form.is_valid())

        data['unit'] = self.unit.pk
        form = RecipeIngredientForm(data=data)
        self.assertFalse(form.is_valid())

    def test_fields_filled_in(self):
        """ Ensures that filled in form is considered to be valid """

        data = {'ingredient': self.potato.pk, 'unit': self.unit.pk, 'quantity':
                1.0}
        form = RecipeIngredientForm(data=data)
        self.assertTrue(form.is_valid())

    def test_fields_non_existent_pks(self):
        """
        Ensures that an error is thrown if non-existent PKs are selected.
        Should not be possible to do - but good to check nevertheless.
        """

        data = {'ingredient': 9999, 'unit': 9999, 'quantity': 1}
        form = RecipeIngredientForm(data=data)

        self.assertFalse(form.is_valid())


class AddRecipeFormTests(TestCase):
    """ Test suite to test the AddRecipeForm """

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')

    def test_fields_not_empty(self):
        """ Ensure that information is entered into the fields """

        data = {'author': self.user, 'title': 'test', 'description': 'test'}
        form = AddRecipeFridgeForm(data=data)

        self.assertTrue(form.is_valid())

    def test_fields_empty(self):
        """ Ensure that empty data cannot be passed """

        data = {'title': '   ', 'description': 'test'}
        form = AddRecipeFridgeForm(data=data)

        self.assertFalse(form.is_valid())

        data = {'title': 'test', 'description': ' '}
        form = AddRecipeFridgeForm(data=data)

        self.assertFalse(form.is_valid())

    def test_image_field(self):
        """ Ensure that the form can take image field """

        with open('static/test/test.png', 'rb') as image:
            data = {'title': 'test', 'description': 'testing'}
            image_data = {'image': SimpleUploadedFile(image.name, image.read())}
            form = AddRecipeFridgeForm(data=data, files=image_data)

            self.assertTrue(form.is_valid())
