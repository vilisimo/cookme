from django.test import TestCase
from django.contrib.auth.models import User

from utilities.populate import (
    get_user,
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

        self.assertEqual(u1, u2)


