"""
Test suite for custom admin functions.
"""


from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.admin.sites import AdminSite

from ingredients.models import Ingredient
from recipes.models import Recipe
from .models import Fridge, FridgeIngredient
from .admin import FridgeAdmin


class FridgeAdminTests(TestCase):
    """
    Test suite to ensure that custom functionality in Fridge admin panel
    works as expected.
    """

    def setUp(self):
        self.user = User.objects.create_user(username='test')
        self.fridge = Fridge.objects.create(user=self.user)
        self.site = AdminSite()

    def test_ingredient_list(self):
        """ Test to ensure that ingredient list shows up properly. """

        i1 = Ingredient.objects.create(name='Apple', type='Fruit')
        i2 = Ingredient.objects.create(name='Orange', type='Fruit')
        FridgeIngredient.objects.create(fridge=self.fridge, ingredient=i1)
        FridgeIngredient.objects.create(fridge=self.fridge, ingredient=i2)

        expected = ", ".join([i1.name, i2.name])
        fa = FridgeAdmin(Fridge, self.site)

        self.assertEqual(fa.ingredient_list(self.fridge), expected)

    def test_recipes_list(self):
        """ Test to ensure that recipe list shows up properly. """

        r1 = Recipe.objects.create(author=self.user, title='test',
                                   description='test')
        r2 = Recipe.objects.create(author=self.user, title='test2',
                                   description='test2')
        self.fridge.recipes.add(r1)
        self.fridge.recipes.add(r2)

        expected = ", ".join([r1.title, r2.title])
        fa = FridgeAdmin(Fridge, self.site)

        self.assertEqual(fa.recipe_list(self.fridge), expected)
