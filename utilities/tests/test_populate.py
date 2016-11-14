import os
from unittest import mock
from tempfile import NamedTemporaryFile

from django.test import TestCase
from django.contrib.auth.models import User

from ingredients.models import Unit, Ingredient
from recipes.models import Recipe
from utilities.populate import (
    get_user, populate_units, populate_ingredients, populate_recipes, bcolors,
    commit_recipe, commit_recipe_ingredient,
)


class GetUserTests(TestCase):
    """
    Test suite to ensure get_user() works properly and does not break
    from the slightest breeze.
    """

    def test_get_user_no_user(self):
        """
        Ensures that get_user creates a user when the instance does not exist.
        """

        user = get_user('test', 'test')

        self.assertTrue(user)

    def test_user_in_db(self):
        """
        Ensures that the function does not try to create identical copy of a
        user.
        """

        u1 = User.objects.create_user(username='test', password='test')
        u2 = get_user('test', 'test')

        self.assertEquals(u1, u2)

    def test_user_in_db_create_diff_pass(self):
        """
        Ensures that even when different password is passed, there is no
        attempt to try to duplicate the user.

        NOTE: it is impossible to retrieve user's password. Hence, even if we
        pass a different password, the function will return a user, because
        function does not care about the password, only about the username.
        """

        u1 = User.objects.create_user(username='test', password='test1')
        u2 = get_user('test', 'test2')

        self.assertEquals(u1, u2)


class PopulateUnitsTests(TestCase):
    """ Test suite to make sure that unit population goes well. """

    def setUp(self):
        current = os.path.normpath(os.getcwd())
        self.directory = os.path.join(current, 'utilities', 'data')
        self.units_txt = os.path.join(self.directory, 'units.txt')

    def test_units_created(self):
        """ Ensures that units are properly created when the file exists. """

        with open(self.units_txt) as f:
            f.readline()  # Get rid of the line specifying what columns mean
            first = f.readline().split(';')  # Get info about first ingredient.
            first = [item.strip() for item in first]

        name = first[0]
        abbrev = first[1]
        description = first[2]

        populate_units(units_txt=self.units_txt)
        u = Unit.objects.get(name=name, abbrev=abbrev, description=description)

        self.assertTrue(u)

    def test_correct_amount_of_units_created(self):
        """ Ensures that all but one lines are used for the population. """

        with open(self.units_txt) as f:
            for i, l in enumerate(f):
                pass
            expected = i  # Note no +1, since first line should be skipped.

        populate_units(self.units_txt)
        actual_count = len(Unit.objects.all())

        self.assertEquals(expected, actual_count)

    def test_exceptions_raised(self):
        """
        Ensures that TypeError is raised if input file is not provided.
        Ensures that FileNotFoundError is raised if input file is not found.
        """

        with self.assertRaises(TypeError):
            populate_units()

        with self.assertRaises(FileNotFoundError):
            populate_units('does_not_exist.txt')

    def test_empty_file(self):
        """
        Ensures that when empty file is passed in, no units are created. It
        might be more user friendly to throw an error/exception, but since
        I'm the only user, I'll skip that.
        """

        with NamedTemporaryFile() as temp_file:
            populate_units(temp_file.name)
        units = Unit.objects.all()

        self.assertFalse(units)


class PopulateIngredientsTests(TestCase):
    """
    Test suite to ensure that populate_ingredients() does not break when
    someone looks at it.
    """

    def setUp(self):
        current = os.path.normpath(os.getcwd())
        self.directory = os.path.join(current, 'utilities', 'data')
        self.ingredients_txt = os.path.join(self.directory, 'ingredients.txt')

    def test_ingredients_created(self):
        """
        Ensures that file is opened and ingredients are created accordingly.
        """

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
        """
        Ensures that there are as many ingredients as there are lines in the
        text file (-1 for the first line, which has descriptions).
        """

        with open(self.ingredients_txt) as f:
            for i, line in enumerate(f):
                pass
            expected = i

        populate_ingredients(ingredients_txt=self.ingredients_txt)
        ingredients = Ingredient.objects.all()

        self.assertEquals(expected, len(ingredients))

    def test_exceptions_raised(self):
        """
        Ensures that TypeError is raised if input file is not provided.
        Ensures that FileNotFoundError is raised if input file is not found.
        """

        with self.assertRaises(TypeError):
            populate_ingredients()

        with self.assertRaises(FileNotFoundError):
            populate_ingredients('does_not_exist.txt')

    def test_empty_file(self):
        """
        Ensures that when empty file is passed in, no ingredients are created.
        It might be more user friendly to throw an error/exception, but since
        I'm the only user, I'll skip that.
        """

        with NamedTemporaryFile() as temp_file:
            populate_units(temp_file.name)
        ingredients = Ingredient.objects.all()

        self.assertFalse(ingredients)


class TestColourfulPrint(TestCase):
    """ Small test suite to test colourful prints. """

    def test_error(self):
        """ Ensures that error is printed with proper colours. """

        red = '\033[91m'
        text = bcolors.error("text")

        self.assertIn(red, text)

    def test_success(self):
        """ Ensures that success messages are printed in proper colour. """

        blue = '\033[94m'
        text = bcolors.success("text")

        self.assertIn(blue, text)


class CommitRecipeTests(TestCase):
    """
    Ensures that helper function commit_recipe creates a recipe instance,
    commits it to the database, and does not break when a wrong input is
    provided.
    """

    def test_creates_recipe_values_ok(self):
        """ Ensures Recipe object is created when values are correct. """

        values = {
            'author': 'Test',
            'title': 'Test',
            'description': 'Test',
            'cuisine': 'Test',
            'steps': {
                '1': 'First',
                '2': 'Second'
            }
        }
        recipe = commit_recipe(values)

        self.assertTrue(recipe)

    def test_does_not_have_values(self):
        """
        Ensures that when no values are provided, exception is raised and user
        is informed to provide a value (happens only when launching from
        command line, though).
        """

        values = {}
        recipe = None
        with self.assertRaises(KeyError):
            recipe = commit_recipe(values)

        self.assertFalse(recipe)

    def test_does_not_have_one_value(self):
        """
        Ensures that when all but one value (key) is provided, exception is
        raised and user is informed to provide a value.
        """

        values = {
            'author': 'Test',
            'description': 'Test',
            'cuisine': 'Test',
            'steps': {'1': 'First',
                      '2': 'Second'}
        }

        recipe = None
        with self.assertRaises(KeyError):
            recipe = commit_recipe(values)

        self.assertFalse(recipe)


class CommitRecipeIngredientTests(TestCase):
    """
    Ensures that helper function commit_recipe_ingredients creates a
    RecipeIngredient instance, commits it to the database, and does not break
    when a wrong input is provided.
    """

    def setUp(self):
        u = User.objects.create_user(username='test')
        self.r = Recipe.objects.create(author=u, title='test', description='t')

    def test_does_not_have_values(self):
        """
        Ensures that when no values are provided, exception is raised and user
        is informed to provide a value (happens only when launching from
        command line, though).
        """

        values = {}
        recipe_ingredients = []
        with self.assertRaises(KeyError):
            recipe_ingredients = commit_recipe_ingredient(values, self.r)

        self.assertFalse(recipe_ingredients)

    def test_creates_recipe_ingredient_values_ok(self):
        """ Ensures RecipeIngredient is created when values are correct. """

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
    """
    Test suite to ensure populate_recipes() works correctly and handles all
    unusual situations well.
    """

    def setUp(self):
        current = os.path.normpath(os.getcwd())
        self.parent = os.path.join(current, 'utilities', 'data')
        self.directory = os.path.join(self.parent, 'recipes')

    def test_no_folder(self):
        """ Ensure that an exception is raised when the folder is not given. """

        with self.assertRaises(FileNotFoundError):
            populate_recipes()

    def test_empty_folder(self):
        """
        Ensure that when an empty folder is given, no recipes are created.
        Also ensure that nothing is created (nothing should if exception is
        thrown, but you never know...).

        Note that never mind the directory, listdir will return an empty
        list, triggering an error, for which we are testing.
        """

        with mock.patch('utilities.populate.os.listdir') as mocked_listdir:
            mocked_listdir.return_value = []

            with self.assertRaises(FileNotFoundError):
                populate_recipes(self.directory)

            recipes = Recipe.objects.all()
            self.assertFalse(recipes, "Recipes were created after exception!")

    def test_population_with_proper_files(self):
        """
        Ensure that with a proper file recipes are created.
        """

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
