from django.contrib.auth.models import User
from django.core.urlresolvers import resolve
from django.test import TestCase

from fridge.models import Fridge, FridgeIngredient
from ingredients.models import Ingredient, Unit


class FridgeTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test')
        self.fridge = Fridge.objects.create(user=self.user)

    def test_str_representation(self):
        expected = f"{self.user.username}'s fridge"

        actual = str(self.fridge)

        self.assertEqual(expected, actual)

    def test_absolute_url_mapping(self):
        view = resolve(self.fridge.get_absolute_url())

        self.assertEqual(view.view_name, 'fridge:fridge_detail')


class FridgeIngredientTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test')
        self.fridge = Fridge.objects.create(user=self.user)
        self.unit = Unit.objects.create(name='kilogram', abbrev='kg')
        self.ingredient = Ingredient.objects.create(name='Meat', type='Meat')
        self.fi = FridgeIngredient.objects.create(fridge=self.fridge,
                                                  ingredient=self.ingredient,
                                                  unit=self.unit, quantity=1)

    def test_str_representation(self):
        expected = f'{self.ingredient} in {self.fridge}'

        actual = str(self.fi)

        self.assertEquals(expected, actual)
