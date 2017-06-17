from django.test import TestCase

from fridge.forms import FridgeIngredientForm
from ingredients.models import Ingredient, Unit


class FridgeIngredientFormTests(TestCase):
    def setUp(self):
        self.p = Ingredient.objects.create(name='Potato', type='Vegetable')
        self.u = Unit.objects.create(name='kilogram', abbrev='kg')

    def test_fields_non_existent_pks_not_allowed(self):
        data = {'ingredient': 'test', 'unit': 999, 'quantity': 1}

        form = FridgeIngredientForm(data=data)

        self.assertFalse(form.is_valid(), "Form with non-existent PKs was valid.")

    def test_empty_fields_not_allowed(self):
        form = FridgeIngredientForm(data={})

        self.assertFalse(form.is_valid(), "Form with no data was valid.")

    def test_empty_unit_quantity_fields_not_allowed(self):
        data = {'ingredient': 'test'}

        form = FridgeIngredientForm(data=data)

        self.assertFalse(form.is_valid(), "Form without units and quantity "
                                          "was valid.")

    def test_empty_quantity_field_not_allowed(self):
        data = {'ingredient': 'test', 'unit': self.u.pk}

        form = FridgeIngredientForm(data=data)

        self.assertFalse(form.is_valid(), "Form without quantity was valid.")

    def test_negative_values_not_allowed(self):
        data = {'ingredient': 'test', 'unit': self.u.pk, 'quantity': -0.1}
        form = FridgeIngredientForm(data=data)

        self.assertFalse(form.is_valid(), "Negative value was allowed.")

    def test_valid_fields_pass(self):
        data = {'ingredient': 'test', 'unit': self.u.pk, 'quantity': 1.1}

        form = FridgeIngredientForm(data=data)

        self.assertTrue(form.is_valid(), "Correct data threw an error.")
