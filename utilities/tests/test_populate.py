import os
from tempfile import NamedTemporaryFile

from django.test import TestCase
from django.contrib.auth.models import User

from ingredients.models import Unit, Ingredient
from utilities.populate import (
    get_user, populate_units,
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
        self.directory = os.path.normpath(os.getcwd()) + '/utilities/' + 'data/'
        self.units_txt = self.directory + 'units.txt'

    def test_units_created(self):
        """ Ensures that units are properly created when the file exists. """

        with open(self.units_txt) as f:
            f.readline()  # Get rid of the line specifying what columns mean
            info = f.readline().split(';')  # Get info about first ingredient.
            info = [item.strip() for item in info]

        name = info[0]
        abbrev = info[1]
        description = info[2]

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
