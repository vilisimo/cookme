from django.test import TestCase

from recipes.models import Recipe
from fridge.helpers import get_fridge_recipes
from utilities.mock_db import populate_recipes


class TestGetRecipes(TestCase):
    """
    Test cases to ensure that matching recipes against a given ingredient set
    returns an expected result.
    """

    def setUp(self):
        recipes = populate_recipes()
        self.r1 = recipes[0]
        self.r2 = recipes[1]
        self.r3 = recipes[2]
        self.r4 = recipes[3]

    def test_get_recipes_one_ingredient(self):
        """
        Ensures that when only one ingredient is given, only a recipe
        with that one ingredient is returned.
        """

        ingredients = {'meat'}
        recipes = get_fridge_recipes(ingredients)

        self.assertIn(self.r1, recipes)

    def test_get_recipes_two_ingredients(self):
        """
        Ensures that when we there are two ingredients in a set, only those
        recipes that consist of one ingredient or both of them are returned.
        """

        ingredients = {'meat', 'lemon'}
        recipes = get_fridge_recipes(ingredients)
        expected = [self.r1, self.r4]

        self.assertEquals(expected, list(recipes))

    def test_get_recipes_all_ingredients(self):
        """
        Ensures that all recipes are chosen when ingredient list includes all
        possible ingredients.
        """

        ingredients = {'meat', 'lemon', 'apple', 'white bread'}
        recipes = get_fridge_recipes(ingredients)
        expected = Recipe.objects.all()

        self.assertEquals(list(expected), list(recipes))

    def test_non_existent_ingredient(self):
        """ Ensure that non-existent ingredients do not return anything. """

        ingredients = {'fairy dust'}
        recipes = get_fridge_recipes(ingredients)

        self.assertFalse(recipes)

