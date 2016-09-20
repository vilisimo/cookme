from django.test import TestCase

from ingredients.models import Ingredient, Unit
from .forms import FridgeIngredientForm


class FridgeIngredientFormTests(TestCase):
    """ Test suite to ensure that FridgeIngredientForm works correctly. """

    def setUp(self):
        self.p = Ingredient.objects.create(name='Potato', type='Vegetable')
        self.u = Unit.objects.create(name='kilogram', abbrev='kg')

    def test_fields_non_existent_pks(self):
        """ Ensures that form with non-existent primary keys is not valid. """

        data = {'ingredient': 999, 'unit': 999, 'quantity': 1}
        form = FridgeIngredientForm(data=data)

        self.assertFalse(form.is_valid(), "Form with non-existent PKs was "
                                          "valid.")

    def test_fields_empty(self):
        """ Ensure that form with empty fields does not pass. """

        data = dict()
        form = FridgeIngredientForm(data=data)

        self.assertFalse(form.is_valid(), "Form with no data was valid.")

        data['ingredient'] = self.p.pk
        form = FridgeIngredientForm(data=data)

        self.assertFalse(form.is_valid(), "Form without units and quantity "
                                          "was valid.")

        data['unit'] = self.u.pk
        form = FridgeIngredientForm(data=data)

        self.assertFalse(form.is_valid(), "Form without quantity was valid.")

    def test_all_correct(self):
        """ Ensure that correct input is considered to be valid. """

        data = {'ingredient': self.p.pk, 'unit': self.u.pk, 'quantity': 1.1}
        form = FridgeIngredientForm(data=data)

        self.assertTrue(form.is_valid(), "Correct data threw an error.")

    def test_negative_value(self):
        """ Ensure that negative value for quantity is not allowed. """

        data = {'ingredient': self.p.pk, 'unit': self.u.pk, 'quantity': -0.1}
        form = FridgeIngredientForm(data=data)

        self.assertFalse(form.is_valid(), "Negative value was allowed.")

