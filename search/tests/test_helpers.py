"""
Tests to ensure that helper functions are fully operational.
"""

from django.test import TestCase
from django.contrib.auth.models import User

from search.helpers import encode, decode, get_name_set, get_fridge_recipes
from ingredients.models import Unit, Ingredient
from recipes.models import Recipe, RecipeIngredient as RecIng


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


class TestGetRecipes(TestCase):
    """
    Test cases to ensure that matching recipes against a given ingredient set
    returns an expected result.
    """

    def setUp(self):
        user = User.objects.create(username='get_fridge_recipes')

        # Ingredients
        i1 = Ingredient.objects.create(name='Meat', type='Meat')
        i2 = Ingredient.objects.create(name='Lemon', type='Fruit')
        i3 = Ingredient.objects.create(name='Apple', type='Fruit')
        i4 = Ingredient.objects.create(name='White Bread', type='Bread')
        # Units
        u = Unit.objects.create(name='kilogram', abbrev='kg')

        # Recipes
        self.r = Recipe.objects.create(author=user, title='MeatRec')
        RecIng.objects.create(recipe=self.r, ingredient=i1, unit=u, quantity=1)

        self.r2 = Recipe.objects.create(author=user, title='MeatLemonAppleRec')
        RecIng.objects.create(recipe=self.r2, ingredient=i1, unit=u, quantity=1)
        RecIng.objects.create(recipe=self.r2, ingredient=i2, unit=u, quantity=1)
        RecIng.objects.create(recipe=self.r2, ingredient=i3, unit=u, quantity=1)

        self.r3 = Recipe.objects.create(author=user, title="AllIngredientsRec")
        RecIng.objects.create(recipe=self.r3, ingredient=i1, unit=u, quantity=1)
        RecIng.objects.create(recipe=self.r3, ingredient=i2, unit=u, quantity=1)
        RecIng.objects.create(recipe=self.r3, ingredient=i3, unit=u, quantity=1)
        RecIng.objects.create(recipe=self.r3, ingredient=i4, unit=u, quantity=1)

        self.r4 = Recipe.objects.create(author=user, title="LemonRec")
        RecIng.objects.create(recipe=self.r4, ingredient=i2, unit=u, quantity=1)

    def test_get_recipes_one_ingredient(self):
        """
        Ensures that when only one ingredient is given, only a recipe
        with that one ingredient is returned.
        """

        ingredients = {'meat'}
        recipes = get_fridge_recipes(ingredients)

        self.assertIn(self.r, recipes)

    def test_get_recipes_two_ingredients(self):
        """
        Ensures that when we there are two ingredients in a set, only those
        recipes that consist of one ingredient or both of them are returned.
        """

        ingredients = {'meat', 'lemon'}
        recipes = get_fridge_recipes(ingredients)
        expected = [self.r, self.r4]

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

