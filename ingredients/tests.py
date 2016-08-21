from django.test import TestCase

from .models import Ingredient, Unit


class IngredientTestCase(TestCase):
    def setUp(self):
        self.ingredient = Ingredient.objects.create(name='Meat', type='Meat')

    def test_str_representation(self):
        self.assertEqual(str(self.ingredient), self.ingredient.name)


class UnitTestCase(TestCase):
    def setUp(self):
        self.unit = Unit.objects.create(name='kilogram', abbrev='kg')

    def test_str_representation(self):
        unit_str = "{0} ({1})".format(self.unit.name, self.unit.abbrev)
        self.assertEqual(str(self.unit), unit_str)
