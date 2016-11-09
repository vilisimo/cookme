import os
from unittest import mock
from tempfile import NamedTemporaryFile

from django.test import TestCase
from django.contrib.auth.models import User

from ingredients.models import Unit, Ingredient
from recipes.models import Recipe
from utilities.populate import (
    get_user, populate_units, populate_ingredients, populate_recipes,
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

