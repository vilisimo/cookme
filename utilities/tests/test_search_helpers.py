from django.contrib.auth.models import User
from django.test import TestCase

from fridge.models import Fridge
from ingredients.models import Ingredient, Unit
from recipes.models import Recipe, RecipeIngredient as RI
from utilities.mock_db import (
    populate_recipes, populate_fridge_recipes, get_user
)
from utilities.search_helpers import (
    encode, decode, get_name_set, superset_recipes, recipes_containing,
)


class EncodingTests(TestCase):
    def test_one_word(self):
        query = 'oneword'

        generated = encode(query)

        self.assertEqual(query, generated)

    def test_multiple_words(self):
        query = "multiple words"
        query = query.replace(' ', '-')

        generated = encode(query)

        self.assertEqual(query, generated)

    def test_multiple_terms(self):
        query = "multiple words, ingredient, ingredient 2"
        expected = "multiple-words ingredient ingredient-2"

        generated = encode(query)

        self.assertEqual(expected, generated)


class DecodingTests(TestCase):
    def test_one_word(self):
        query = 'oneword'

        decoded = decode(query)

        self.assertEqual(query, decoded)

    def test_multiple_words(self):
        query = 'multiple words'
        encoded = encode(query)

        decoded = decode(encoded)

        self.assertEqual(query, decoded)

    def test_multiple_terms(self):
        query = "multiple words, ingredient, ingredient 2"
        encoded = encode(query)

        decoded = decode(encoded)

        self.assertEqual(query.replace(', ', ','), decoded)


class GetNameSetExtractionTests(TestCase):
    def test_one_word_query_correct_set(self):
        query = 'oneword'
        encoded = encode(query)
        decoded = decode(encoded)
        expected = {'Oneword'}

        names = get_name_set(decoded)

        self.assertEqual(names, expected)

    def test_multiple_word_query_set(self):
        query = 'multi word'
        encoded = encode(query)
        decoded = decode(encoded)
        expected = {'Multi Word'}

        names = get_name_set(decoded)

        self.assertEqual(names, expected)

    def test_multiple_terms_query(self):
        query = 'multiple words, ingredient, ingredient 2'
        encoded = encode(query)
        decoded = decode(encoded)
        expected = {'Multiple Words', 'Ingredient', 'Ingredient 2'}

        names = get_name_set(decoded)

        self.assertEqual(names, expected)


class SupersetRecipesTests(TestCase):
    def setUp(self):
        recipes = populate_recipes()
        # Name denotes which ingredients are used for recipe
        self.meat = recipes[0]
        self.meat_lemon_apple = recipes[1]
        self.meat_lemon_apple_bread = recipes[2]
        self.lemon = recipes[3]

    def test_recipes_containing_ingredient_are_returned(self):
        ingredients = {'Meat'}
        expected = [self.meat, self.meat_lemon_apple, self.meat_lemon_apple_bread]

        recipes = superset_recipes(ingredients)

        self.assertEqual(len(expected), len(recipes))
        self.assertTrue(set(expected) == set(recipes))

    def test_recipes_containing_both_ingredients_are_returned(self):
        ingredients = {'Meat', 'Lemon'}
        expected = [self.meat_lemon_apple, self.meat_lemon_apple_bread]

        recipes = superset_recipes(ingredients)

        self.assertEqual(len(expected), len(recipes))
        self.assertTrue(set(expected) == set(recipes))

    def test_two_ingredients_no_matching_recipes(self):
        ingredients = {'White Bread', 'Fairy Dust'}

        recipes = superset_recipes(ingredients)

        self.assertFalse(recipes)

    def test_passing_empty_set(self):
        ingredients = set()
        recipes = superset_recipes(ingredients)

        self.assertFalse(recipes)

    def test_recipes_containing_all_ingredients_returned(self):
        ingredients = {'White Bread', 'Meat', 'Lemon', 'Apple'}
        expected = [self.meat_lemon_apple_bread]

        recipes = superset_recipes(ingredients)

        self.assertEqual(len(expected), len(recipes))
        self.assertTrue(set(expected) == set(recipes))


class SubsetRecipesTests(TestCase):
    def setUp(self):
        recipes = populate_recipes()
        # Name denotes which ingredients are used for recipe
        self.meat = recipes[0]
        self.meat_lemon_apple = recipes[1]
        self.meat_lemon_apple_bread = recipes[2]
        self.lemon = recipes[3]

    def test_returns_recipe_with_only_one_ingredient(self):
        ingredients = {'meat'}

        # Recipes that have more ingredients shouldn't be picked up
        recipes = recipes_containing(ingredients)

        self.assertIn(self.meat, recipes)
        self.assertEqual(len(recipes), 1)

    def test_returns_recipes_with_only_two_ingredients(self):
        ingredients = {'meat', 'lemon'}
        expected = [self.meat, self.lemon]

        recipes = recipes_containing(ingredients)

        self.assertEquals(expected, list(recipes))

    def test_returns_recipes_with_all_ingredients(self):
        ingredients = {'meat', 'lemon', 'apple', 'white bread'}
        expected = Recipe.objects.all()

        recipes = recipes_containing(ingredients)

        self.assertEquals(list(expected), list(recipes))

    def test_non_existent_ingredient(self):
        ingredients = {'fairy dust'}

        recipes = recipes_containing(ingredients)

        self.assertFalse(recipes)


class SubsetRecipesWithFridgeTests(TestCase):
    def setUp(self):
        user = get_user(username='test', password='test')
        recipes = populate_recipes()
        populate_fridge_recipes()
        self.meat = recipes[0]
        self.meat_lemon_apple = recipes[1]
        self.meat_lemon_apple_bread = recipes[2]
        self.lemon = recipes[3]
        self.fridge = Fridge.objects.get(user=user)

    def test_returns_recipe_with_only_one_ingredient(self):
        ingredients = {'meat'}
        recipes = recipes_containing(ingredients, self.fridge)

        self.assertEqual(1, len(recipes))
        self.assertIn(self.meat, recipes)

    def test_returns_recipes_with_only_two_ingredients(self):
        ingredients = {'meat', 'lemon'}
        expected = [self.meat, self.lemon]

        recipes = recipes_containing(ingredients, self.fridge)

        self.assertEquals(expected, list(recipes))

    def test_returns_recipes_with_all_ingredients(self):
        ingredients = {'meat', 'lemon', 'apple', 'white bread'}
        expected = Recipe.objects.all()

        recipes = recipes_containing(ingredients, self.fridge)

        self.assertEquals(list(expected), list(recipes))

    def test_non_existent_ingredient(self):
        ingredients = {'fairy dust'}

        recipes = recipes_containing(ingredients, self.fridge)

        self.assertFalse(recipes)

    def test_more_recipes_than_in_fridge(self):
        # Prepare for creation of a new recipe
        user = User.objects.create_user(username='test2', password='test2')
        i1 = Ingredient.objects.get_or_create(name='Meat', type='Meat')[0]
        i2 = Ingredient.objects.get_or_create(name='Lemon', type='Fruit')[0]
        u = Unit.objects.get(abbrev='kg')

        # Create a unique recipe that does not belong to user 'test'
        r1 = Recipe.objects.get_or_create(author=user, title='Meatlemonrec')[0]
        RI.objects.get_or_create(recipe=r1, ingredient=i1, unit=u, quantity=1)
        RI.objects.get_or_create(recipe=r1, ingredient=i2, unit=u, quantity=1)

        # Get all recipes and recipes that are added to test user's fridge
        # and ensure that the first one is only one larger than the second one.
        fridge_recipes = self.fridge.recipes.all()
        all_recipes = Recipe.objects.all()

        self.assertEqual(len(all_recipes), len(fridge_recipes) + 1)

        # Now get all matching recipes, exclude the new recipe from a list of
        # all recipes and make sure the lists are the same.
        ingredients = {'meat', 'lemon', 'apple', 'white bread'}
        all_recipes = all_recipes.exclude(title='Meatlemonrec')
        recipes = recipes_containing(ingredients, self.fridge)

        self.assertEqual(list(all_recipes), list(recipes))

    def test_no_matches_when_no_recipes_in_fridge(self):
        ingredients = {'meat', 'lemon', 'apple', 'white bread'}
        self.fridge.recipes.all().delete()

        recipes = recipes_containing(ingredients, self.fridge)

        self.assertFalse(recipes)

    def test_less_recipes_in_fridge_than_globally(self):
        ingredients = {'meat', 'lemon', 'apple', 'white bread'}
        self.fridge.recipes.remove(self.meat)
        self.fridge.recipes.remove(self.meat_lemon_apple)
        fridge_recipes = self.fridge.recipes.all()

        recipes = recipes_containing(ingredients, self.fridge)

        self.assertEqual(list(recipes), list(fridge_recipes))

