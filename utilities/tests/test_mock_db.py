from django.contrib.auth.models import User
from django.test import TestCase

from fridge.models import FridgeIngredient, Fridge
from ingredients.models import Ingredient, Unit
from recipes.models import Recipe
from utilities.mock_db import (
    populate_recipes, populate_ingredients, populate_units,
    populate_fridge_ingredients, populate_fridge_recipes, logged_in_client,
)


class PopulateRecipesTests(TestCase):
    def test_populate_recipes_returns_created_recipes(self):
        recipes = populate_recipes()

        self.assertTrue(len(recipes) > 0)

    def test_populate_recipes_does_not_create_more_recipes_than_returned(self):
        recipes = populate_recipes()
        database_recipes = Recipe.objects.all()

        self.assertEquals(list(recipes), list(database_recipes))

    def test_populate_recipe_multiple_calls_creates_one_set_of_recipes(self):
        expected = len(populate_recipes())
        populate_recipes()
        actual = len(Recipe.objects.all())

        self.assertEquals(expected, actual)


class PopulateIngredientsTests(TestCase):
    def test_populate_ingredients_returns_ingredients(self):
        ingredients = populate_ingredients()

        self.assertTrue(len(ingredients) > 0)

    def test_populate_ingredients_does_not_create_more_than_returned(self):
        ingredients = populate_ingredients()
        database_ingredients = Ingredient.objects.all()

        self.assertEquals(list(ingredients), list(database_ingredients))


class PopulateUnitsTests(TestCase):
    def test_populate_units_returns_units(self):
        units = populate_units()

        self.assertTrue(len(units) > 0)

    def test_populate_units_does_not_create_more_units_than_returned(self):
        units = populate_units()
        database_units = Unit.objects.all()

        self.assertEquals(list(units), list(database_units))


class PopulateFridgeIngredientsTests(TestCase):
    def test_populate_fridge_ingredients_returns_fridge_ingredients(self):
        fridge_ingredients = populate_fridge_ingredients()

        self.assertTrue(len(fridge_ingredients) > 0)

    def test_populate_fis_does_not_create_more_fis_than_returned(self):
        fridge_ingredients = populate_fridge_ingredients()
        database_fridge_ingredients = FridgeIngredient.objects.all()

        self.assertEqual(list(fridge_ingredients), list(database_fridge_ingredients))


class PopulateFridgeRecipesTests(TestCase):
    def test_populate_fridge_recipes_returns_fridge_recipes(self):
        fridge_recipes = populate_fridge_recipes()

        self.assertTrue(len(fridge_recipes) > 0)

    def test_populate_does_not_create_more_recipes_than_returned(self):
        fridge_recipes = populate_fridge_recipes()
        user = User.objects.get(username='test')
        fridge = Fridge.objects.get(user=user)
        in_db = fridge.recipes.all()

        self.assertEqual(list(fridge_recipes), list(in_db))


class OtherFunctionalityTests(TestCase):
    def test_logged_in_client_accepts_user(self):
        user = User.objects.create_user(username='bu', password='pu')
        client = logged_in_client(user)

        # Simply assert that it exists. If it does, function works.
        self.assertTrue(client)
