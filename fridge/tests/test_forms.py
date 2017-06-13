from django.test import TestCase

from fridge.forms import FridgeIngredientForm
from ingredients.models import Ingredient, Unit


class FridgeIngredientFormTests(TestCase):
    """
    Test suite to ensure that FridgeIngredientForm works correctly. That is,
    that it does not allow empty forms, negative values, etc.
    """

    def setUp(self):
        self.p = Ingredient.objects.create(name='Potato', type='Vegetable')
        self.u = Unit.objects.create(name='kilogram', abbrev='kg')

    def test_fields_non_existent_pks(self):
        """ Ensures that a form with non-existent primary keys is not valid. """

        data = {'ingredient': 'test', 'unit': 999, 'quantity': 1}
        form = FridgeIngredientForm(data=data)

        self.assertFalse(form.is_valid(), "Form with non-existent PKs was "
                                          "valid.")

    def test_fields_empty(self):
        """ Ensure that a form with empty fields does not pass. """

        data = dict()
        form = FridgeIngredientForm(data={})

        self.assertFalse(form.is_valid(), "Form with no data was valid.")

    def test_no_unit_quantity_fields(self):
        """
        Ensure that a form without unit and quantity fields filled in is
        not valid.
        """

        data = {'ingredient': 'test'}
        form = FridgeIngredientForm(data=data)

        self.assertFalse(form.is_valid(), "Form without units and quantity "
                                          "was valid.")

    def test_no_quantity_field(self):
        """ Ensure that a form with quantity field empty is not valid. """

        data = {
            'ingredient': 'test',
            'unit': self.u.pk,
        }
        form = FridgeIngredientForm(data=data)

        self.assertFalse(form.is_valid(), "Form without quantity was valid.")

    def test_all_correct(self):
        """ Ensure that correct input is considered to be valid. """

        data = {'ingredient': 'test', 'unit': self.u.pk, 'quantity': 1.1}
        form = FridgeIngredientForm(data=data)

        self.assertTrue(form.is_valid(), "Correct data threw an error.")

    def test_negative_value(self):
        """ Ensure that negative value for quantity is not allowed. """

        data = {'ingredient': 'test', 'unit': self.u.pk, 'quantity': -0.1}
        form = FridgeIngredientForm(data=data)

        self.assertFalse(form.is_valid(), "Negative value was allowed.")

