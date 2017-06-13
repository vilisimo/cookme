"""
Test suite for custom admin functions.
"""


from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.test import TestCase

from fridge.admin import FridgeAdmin
from fridge.models import Fridge, FridgeIngredient
from ingredients.models import Ingredient, Unit
from recipes.models import Recipe


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
        """
        Test to ensure that ingredient list shows up in admin panel and
        contains all the ingredients that it should contain.
        """

        u = Unit.objects.create(name='kilogram', abbrev='kg')
        i1 = Ingredient.objects.create(name='Apple', type='Fruit')
        i2 = Ingredient.objects.create(name='Orange', type='Fruit')
        FridgeIngredient.objects.create(fridge=self.fridge, ingredient=i1,
                                        unit=u, quantity=1)
        FridgeIngredient.objects.create(fridge=self.fridge, ingredient=i2,
                                        unit=u, quantity=1)

        expected = ", ".join([i1.name, i2.name])
        fa = FridgeAdmin(Fridge, self.site)

        self.assertEqual(fa.ingredient_list(self.fridge), expected)

    def test_recipes_list(self):
        """
        Test to ensure that recipe list shows up properly in admin panel and
        contains all the recipes that it should contain.
        """

        r1 = Recipe.objects.create(author=self.user, title='test',
                                   description='test')
        r2 = Recipe.objects.create(author=self.user, title='test2',
                                   description='test2')
        self.fridge.recipes.add(r1)
        self.fridge.recipes.add(r2)

        expected = ", ".join([r1.title, r2.title])
        fa = FridgeAdmin(Fridge, self.site)

        self.assertEqual(fa.recipe_list(self.fridge), expected)
