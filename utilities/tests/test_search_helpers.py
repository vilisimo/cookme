"""
Tests to ensure that helper functions are fully operational.
"""

from django.test import TestCase

from recipes.models import Recipe

from utilities.mock_db import populate_recipes
from utilities.search_helpers import (
    encode, decode, get_name_set, superset_recipes, subset_recipes
)


class EncodingTests(TestCase):
    """
    Test suite to ensure that function producing query string works.
    """

    def test_one_word(self):
        """ Ensures that one word query strings are constructed properly. """

        query = 'oneword'
        generated = encode(query)

        self.assertEqual(query, generated)

    def test_multiple_words(self):
        """ Ensures that multi-word queries are formatted properly. """

        query = "multiple words"
        generated = encode(query)
        query = query.replace(' ', '-')

        self.assertEqual(query, generated)

    def test_multiple_terms(self):
        """
        Ensures that multiple terms that may contain multi-word ingredients /
        recipes are formatted properly.

        Reminder: spaces between multi-word ingredients/recipes should be
        replaced by dashes.
        """

        query = "multiple words, ingredient, ingredient 2"
        expected = "multiple-words ingredient ingredient-2"
        generated = encode(query)

        self.assertEqual(expected, generated)


class DecodingTests(TestCase):
    """
    Test suite to ensure that decoding of query strings produces a correct
    result.
    """

    def test_one_word(self):
        """ Ensures that decoding does not mess up one word queries. """

        query = 'oneword'
        decoded = decode(query)

        self.assertEqual(query, decoded)

    def test_multiple_words(self):
        """ Ensures that decoding does not mess up multi-word queries. """

        query = 'multiple words'
        encoded = encode(query)
        decoded = decode(encoded)

        self.assertEqual(query, decoded)

    def test_multiple_terms(self):
        """
        Ensures that decoding does not mess up queries with multiple terms.

        Note that the space removal after comma is intentional. It is the
        expected functionality of decode function, as it makes processing
        later easier.
        """

        query = "multiple words, ingredient, ingredient 2"
        encoded = encode(query)
        decoded = decode(encoded)

        self.assertEqual(query.replace(', ', ','), decoded)


class GetNameSetExtractionTests(TestCase):
    """
    Test suite to ensure that a set of names extracted from decoding query is
    correct.
    """

    def test_one(self):
        """ Ensures that one word query results in a correct set. """

        query = 'oneword'
        encoded = encode(query)
        decoded = decode(encoded)
        names = get_name_set(decoded)
        expected = {'Oneword'}

        self.assertEqual(names, expected)

    def test_multiple_words(self):
        """ Ensures that processing multi-word queries returns a correct set """

        query = 'multi word'
        encoded = encode(query)
        decoded = decode(encoded)
        names = get_name_set(decoded)
        expected = {'Multi Word'}

        self.assertEqual(names, expected)

    def test_multiple_terms(self):
        """
        Ensures that processing a query with multiple terms returns a correct
        set.
        """

        query = 'multiple words, ingredient, ingredient 2'
        encoded = encode(query)
        decoded = decode(encoded)
        names = get_name_set(decoded)
        expected = {'Multiple Words', 'Ingredient', 'Ingredient 2'}

        self.assertEqual(names, expected)


class SupersetRecipesTests(TestCase):
    """
    Test suite to ensure that the superset_recipes function produces correct
    results with given sets of strings.
    """

    def setUp(self):
        recipes = populate_recipes()
        self.r1 = recipes[0]  # Ingredients: Meat
        self.r2 = recipes[1]  # Ingredients: Meat, Lemon, Apple
        self.r3 = recipes[2]  # Ingredients: Meat, Lemon, Apple, White Bread
        self.r4 = recipes[3]  # Ingredients: Lemon

    def test_one_ingredient(self):
        """
        Ensures that all recipes containing specified ingredient are returned.
        """

        ingredients = {'Meat'}
        expected = [self.r1, self.r2, self.r3]
        recipes = superset_recipes(ingredients)

        self.assertEqual(len(expected), len(recipes))
        self.assertTrue(set(expected) == set(recipes))

    def test_two_ingredients(self):
        """
        Ensures that only recipes that have two of the specified ingredients are
        returned. Note that only those recipes that have BOTH ingredient should
        be shown.
        """

        ingredients = {'Meat', 'Lemon'}
        expected = [self.r2, self.r3]
        recipes = superset_recipes(ingredients)

        self.assertEqual(len(expected), len(recipes))
        self.assertTrue(set(expected) == set(recipes))

    def test_two_ingredients_no_recipes(self):
        """
        Ensures that when two ingredients are supplied and no recipe has a
        combination of them, no recipes are returned.
        """

        ingredients = {'White Bread', 'Fairy Dust'}
        recipes = superset_recipes(ingredients)

        self.assertFalse(recipes)

    def test_empty(self):
        """ Ensure nothing is returned when an empty set is passed in. """

        ingredients = set()
        recipes = superset_recipes(ingredients)

        self.assertFalse(recipes)

    def test_all_ingredients(self):
        """
        Ensure that when all possible ingredients are supplied,
        only recipes with them are returned.
        """

        ingredients = {'White Bread', 'Meat', 'Lemon', 'Apple'}
        expected = [self.r3]
        recipes = superset_recipes(ingredients)

        self.assertEqual(len(expected), len(recipes))
        self.assertTrue(set(expected) == set(recipes))


class SubsetRecipesTests(TestCase):
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
        recipes = subset_recipes(ingredients)

        self.assertIn(self.r1, recipes)

    def test_get_recipes_two_ingredients(self):
        """
        Ensures that when we there are two ingredients in a set, only those
        recipes that consist of one ingredient or both of them are returned.
        """

        ingredients = {'meat', 'lemon'}
        recipes = subset_recipes(ingredients)
        expected = [self.r1, self.r4]

        self.assertEquals(expected, list(recipes))

    def test_get_recipes_all_ingredients(self):
        """
        Ensures that all recipes are chosen when ingredient list includes all
        possible ingredients.
        """

        ingredients = {'meat', 'lemon', 'apple', 'white bread'}
        recipes = subset_recipes(ingredients)
        expected = Recipe.objects.all()

        self.assertEquals(list(expected), list(recipes))

    def test_non_existent_ingredient(self):
        """ Ensure that non-existent ingredients do not return anything. """

        ingredients = {'fairy dust'}
        recipes = subset_recipes(ingredients)

        self.assertFalse(recipes)