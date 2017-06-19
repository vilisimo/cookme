import os
from tempfile import NamedTemporaryFile
from unittest import mock

from django.contrib.auth.models import User
from django.test import TestCase

from ingredients.models import Unit, Ingredient
from recipes.models import Recipe
from utilities.populate import (
    get_user, populate_units, populate_ingredients, populate_recipes, bcolors,
    commit_recipe, commit_recipe_ingredient,
)


class GetUserTests(TestCase):
    def test_get_user_creates_user_when_it_doesnt_exist(self):
        user = get_user('test', 'test')

        self.assertTrue(user)

    def test_doesnt_create_same_user_twice(self):
        u1 = User.objects.create_user(username='test', password='test')
        u2 = get_user('test', 'test')

        self.assertEquals(u1, u2)

    def test_get_user_ignores_different_passwords(self):
        """
        Ensures that even when different password is passed, there is no
        attempt to try to duplicate the user.

        NOTE: it is impossible to retrieve user's password. Hence, even if we
        pass a different password, the function will return a user, because it
        does not care about the password.
        """

        u1 = User.objects.create_user(username='test', password='test1')
        u2 = get_user('test', 'test2')

        self.assertEquals(u1, u2)


class PopulateUnitsTests(TestCase):
    def setUp(self):
        current = os.path.normpath(os.getcwd())
        self.directory = os.path.join(current, 'utilities', 'data')
        self.units_txt = os.path.join(self.directory, 'units.txt')

    def test_units_created(self):
        with open(self.units_txt) as f:
            f.readline()  # Get rid of the line specifying what columns mean
            first = f.readline().split(';')  # Get info about first ingredient.
            first = [item.strip() for item in first]

        name = first[0]
        abbrev = first[1]
        plural = first[2]
        description = first[3]

        populate_units(units_txt=self.units_txt)
        u = Unit.objects.get(name=name, abbrev=abbrev, description=description, plural=plural)

        self.assertTrue(u)

    def test_correct_amount_of_units_created(self):
        expected = count_lines(self.units_txt)
        populate_units(self.units_txt)
        actual_count = len(Unit.objects.all())

        self.assertEquals(expected, actual_count)

    def test_raises_type_error_without_file(self):
        with self.assertRaises(TypeError):
            populate_units()

    def test_raises_type_error_with_non_existent_file(self):
        with self.assertRaises(FileNotFoundError):
            populate_units('does_not_exist.txt')

    def test_empty_file_does_not_create_anything(self):
        with NamedTemporaryFile() as temp_file:
            populate_units(temp_file.name)
        units = Unit.objects.all()

        self.assertFalse(units)


class PopulateIngredientsTests(TestCase):
    def setUp(self):
        current = os.path.normpath(os.getcwd())
        self.directory = os.path.join(current, 'utilities', 'data')
        self.ingredients_txt = os.path.join(self.directory, 'ingredients.txt')

    def test_ingredients_created(self):
        with open(self.ingredients_txt) as f:
            f.readline()
            first = f.readline().split(';')  # Get info about first ingredient.
            first = [item.strip() for item in first]

        name = first[0]
        kind = first[1]
        desc = first[2]

        populate_ingredients(ingredients_txt=self.ingredients_txt)
        i = Ingredient.objects.get(name=name, type=kind, description=desc)

        self.assertTrue(i)

    def test_correct_amount_of_ingredients_created(self):
        expected = count_lines(self.ingredients_txt)

        populate_ingredients(ingredients_txt=self.ingredients_txt)
        ingredients = Ingredient.objects.all()

        self.assertEquals(expected, len(ingredients))

    def test_type_error_raised(self):
        with self.assertRaises(TypeError):
            populate_ingredients()

    def test_not_found_raised(self):
        with self.assertRaises(FileNotFoundError):
            populate_ingredients('does_not_exist.txt')

    def test_empty_file_does_not_create_anything(self):
        with NamedTemporaryFile() as temp_file:
            populate_units(temp_file.name)
        ingredients = Ingredient.objects.all()

        self.assertFalse(ingredients)


class TestColourfulPrint(TestCase):
    def test_error(self):
        red = '\033[91m'
        text = bcolors.error("text")

        self.assertIn(red, text)

    def test_success(self):
        blue = '\033[94m'
        text = bcolors.success("text")

        self.assertIn(blue, text)


class CommitRecipeTests(TestCase):
    def test_creates_recipe_when_values_ok(self):
        values = {
            'author': 'Test',
            'title': 'Test',
            'description': 'Test',
            'cuisine': 'Test',
            'steps': {
                '1': 'First',
                '2': 'Second'
            },
            'picture': 'recipes/small-pot.jpeg'
        }
        recipe = commit_recipe(values)

        self.assertTrue(recipe)

    def test_exception_when_no_values(self):
        values = {}
        recipe = None
        with self.assertRaises(KeyError):
            recipe = commit_recipe(values)

        self.assertFalse(recipe)

    def test_when_dict_does_not_have_one_value(self):
        values = {
            'author': 'Test',
            'description': 'Test',
            'cuisine': 'Test',
            'steps': {'1': 'First',
                      '2': 'Second'},
            'picture': 'recipes/small-pot.jpeg'
        }

        with self.assertRaises(KeyError):
            commit_recipe(values)


class CommitRecipeIngredientTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='test')
        self.r = Recipe.objects.create(author=user, title='test', description='t')

    def test_does_not_have_values(self):
        values = {}
        recipe_ingredients = []
        with self.assertRaises(KeyError):
            recipe_ingredients = commit_recipe_ingredient(values, self.r)

        self.assertFalse(recipe_ingredients)

    def test_creates_recipe_ingredient_values_ok(self):
        Ingredient.objects.create(name='test', type='Bread')
        Ingredient.objects.create(name='test2', type='Bread')
        Unit.objects.create(name='kilogram', abbrev='kg')
        Unit.objects.create(name='unit(s)', abbrev='unit(s)')

        values = {
            'ingredients': {
                'test': '1 unit(s)',
                'test2': '2 kg',
            }
        }
        ris = commit_recipe_ingredient(values, self.r)

        self.assertTrue(ris)


class PopulateRecipes(TestCase):
    def setUp(self):
        current = os.path.normpath(os.getcwd())
        self.parent = os.path.join(current, 'utilities', 'data')
        self.directory = os.path.join(self.parent, 'recipes')

    def test_no_folder_given(self):
        with self.assertRaises(FileNotFoundError):
            populate_recipes()

    def test_no_recipes_when_empty_folder_given(self):
        with mock.patch('utilities.populate.os.listdir') as mocked_listdir:
            mocked_listdir.return_value = []

            with self.assertRaises(FileNotFoundError):
                populate_recipes(self.directory)

            recipes = Recipe.objects.all()
            self.assertFalse(recipes, "Recipes were created after exception!")

    def test_population_creates_recipes_with_proper_files(self):
        count = len(os.listdir(self.directory))
        populate_ingredients(os.path.join(self.parent, 'ingredients.txt'))
        populate_units(os.path.join(self.parent, 'units.txt'))
        populate_recipes(self.directory)
        recipes = len(Recipe.objects.all())

        self.assertEquals(count, recipes)

    # Many more tests needed for populate_recipes(), e.g.:
    #     1. What happens if YAML file is empty?
    #     2. What happens if it is not empty, but some values are missing?
    #     3. What happens if values are not missing, but they are empty?


def count_lines(text_file):
    with open(text_file) as f:
        for index, line in enumerate(f):
            pass
    return index

