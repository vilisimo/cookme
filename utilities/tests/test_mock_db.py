from django.test import TestCase
from django.contrib.auth.models import User

from recipes.models import Recipe
from ingredients.models import Ingredient, Unit
from fridge.models import FridgeIngredient

from utilities.mock_db import (
    populate_recipes, populate_ingredients, populate_units,
    populate_fridge_ingredients, logged_in_client,
)


class MockDatabaseTests(TestCase):
    """
    Test suite to ensure that mock database population really does populate
    database.
    """

    def test_populate_recipes_returns_recipes(self):
        """
        Ensures that populate_recipes() returns recipes that were
        created.
        """

        recipes = populate_recipes()

        self.assertTrue(len(recipes) > 0)

    def test_populate_recipes_does_not_create_more_recipes_than_returned(self):
        """
        Ensures that recipes returned are the only ones created, and that
        there are no more or less of them than that.
        """

        recipes = populate_recipes()
        in_db = Recipe.objects.all()

        self.assertEquals(list(recipes), list(in_db))

    def test_populate_ingredients_returns_ingredients(self):
        """
        Ensures that populate_ingredients() returns ingredients created.
        """

        ingredients = populate_ingredients()

        self.assertTrue(len(ingredients) > 0)

    def test_populate_ings_does_not_create_more_ings_than_returned(self):
        """
        Ensures that ingredients returned are the only ones created, and that
        there are no more or less of them than that.
        """

        ingredients = populate_ingredients()
        in_db = Ingredient.objects.all()

        self.assertEquals(list(ingredients), list(in_db))

    def test_populate_units_returns_units(self):
        """
        Ensures that populate_units() returns units created.
        """

        units = populate_units()

        self.assertTrue(len(units) > 0)

    def test_populate_units_does_not_create_more_units_than_returned(self):
        """
        Ensures that units returned are the only ones created, and that there
        are no more or less of them than that.
        """

        units = populate_units()
        in_db = Unit.objects.all()

        self.assertEquals(list(units), list(in_db))

    def test_populate_fridge_ingredients_returns_fridge_ingredients(self):
        """
        Ensures that populate_fridge_ingredients() returns ingredients created.
        """

        fridge_ingredients = populate_fridge_ingredients()

        self.assertTrue(len(fridge_ingredients) > 0)

    def test_populate_fis_does_not_create_more_fis_than_returned(self):
        """
        Ensures that units returned are the only ones created, and that there
        are no more or less of them than that.
        """

        fridge_ingredients = populate_fridge_ingredients()
        in_db = FridgeIngredient.objects.all()

        self.assertEqual(list(fridge_ingredients), list(in_db))

    def test_logged_in_client_accepts_user(self):
        """
        Ensures logged in client is truly logged in.

        Note: user is not required to be in DB to log in the client...
        """

        user = User.objects.create_user(username='bu', password='pu')
        client = logged_in_client(user)

        # Simply assert that it exists. If it does, function works.
        self.assertTrue(client)
