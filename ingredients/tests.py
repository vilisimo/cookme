from django.test import TestCase

from .models import Ingredient


class IngredientTestCase(TestCase):
    def setUp(self):
        Ingredient.objects.create(name='Meat', type='Meat')

    def test_str_representation(self):
        ingredient = Ingredient.objects.get(name='Meat')
        self.assertEqual(str(ingredient), ingredient.name)
