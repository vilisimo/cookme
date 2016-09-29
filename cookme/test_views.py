"""
Tests to ensure everything in cookme.views works correctly.
"""

from django.test import TestCase
from django.contrib import auth
from django.core.urlresolvers import reverse, resolve
from django.contrib.auth.models import User
from django.test.client import Client

from .views import home, register


class HomePageTests(TestCase):
    """ Test suite to ensure that home page functions properly. """

    def setUp(self):
        self.url = reverse('home')
        self.user = User.objects.create_user(username='test', password='test')
        self.logged = Client()
        self.logged.login(username='test', password='test')

    def test_correct_root_url_resolves_to_home_function(self):
        """
        Test suite to ensure that the root URL is mapped to correct view.
        """

        view = resolve('/')

        self.assertEqual(view.view_name, 'home')
        self.assertEqual(view.func, home)

    def test_anonymous_visit(self):
        """ Test to ensure anonymous users do not see link to a fridge. """

        response = Client().get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Fridge')

    def test_logged_visit(self):
        """ Test to ensure that logged in user sees the fridge. """

        response = self.logged.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Fridge')


class RegisterViewTests(TestCase):
    """ Test suite to ensure register view functions properly. """

    def setUp(self):
        self.client = Client()
        self.url = reverse('register')

    def test_correct_url(self):
        """ Ensures that a correct URL is mapped to a view. """
        
        view = resolve('/accounts/register/')

        self.assertEqual(view.view_name, 'register')
        self.assertEqual(view.func, register)

    def test_can_access_register_view(self):
        """ Ensures that user can access a view. """

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_has_form(self):
        """ Ensures a register form is shown. """

        response = self.client.get(self.url)

        self.assertTrue(response.context['form'])

    def test_registered_user_redirected(self):
        """ Ensures a registered user is redirected from a register view. """

        User.objects.create_user(username='test', password='test')
        client = Client()
        client.login(username='test', password='test')
        response = client.get(self.url)

        self.assertRedirects(response, reverse('home'), status_code=302)

    def test_valid_data_redirect(self):
        """ Ensures that upon valid data submission user is redirected. """

        data = {
            'username': 'ElaborateUsername',
            'password1': 'VerySecretPassword',
            'password2': 'VerySecretPassword'
        }
        response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, 302)

    def test_valid_data_user_created(self):
        """ Ensures a user is created when valid data is submitted. """

        data = {
            'username': 'ElaborateUsername',
            'password1': 'VerySecretPassword',
            'password2': 'VerySecretPassword'
        }
        self.client.post(self.url, data=data)
        user = User.objects.get(username='ElaborateUsername')

        self.assertTrue(user)

    def test_valid_data_user_logged_in(self):
        """ Ensures that upon submission of valid data, user is logged in. """

        data = {
            'username': 'ElaborateUsername',
            'password1': 'VerySecretPassword',
            'password2': 'VerySecretPassword',
        }
        self.client.post(self.url, data=data)
        user = auth.get_user(self.client)

        assert user.is_authenticated()
        # Just to make sure we are really logged in.
        response = self.client.get(reverse('fridge:fridge_detail'))

        self.assertEqual(response.status_code, 200)

    def test_username_exists(self):
        """ Ensures that no duplicate accounts can be created. """

        User.objects.create_user(username='ElaborateUsername',
                                 password='VerySecretPassword')
        data = {
            'username': 'ElaborateUsername',
            'password1': 'VerySecretPassword',
            'password2': 'VerySecretPassword',
        }
        response = self.client.post(self.url, data=data)

        self.assertTrue(response.status_code != 302)


class LoginTests(TestCase):
    """
    Test suite to ensure login works correctly. Although at the moment
    Django's login functionality is used, it may change in the future,
    and thus it is a good idea to write basic tests to ensure it works.
    """

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.url = reverse('login')
        self.client = Client()

    def test_invalid_data(self):
        """
        Ensures that upon submission of invalid data, user is not logged in.
        """

        data = {
            'username': 'test',
            'password': 'testing',
        }

        response = self.client.post(self.url, data=data)
        user = auth.get_user(self.client)

        self.assertNotEqual(response.status_code, 302)
        assert (not user.is_authenticated())

    def test_valid_data(self):
        """ Ensures that upon submitting valid data, user can log in. """

        data = {
            'username': 'test',
            'password': 'test',
        }

        response = self.client.post(self.url, data=data)
        user = auth.get_user(self.client)

        self.assertEqual(response.status_code, 302)
        assert user.is_authenticated()

    def test_missing_data(self):
        """ Ensure that not filling in some fields is not allowed. """

        data = {'username': 'test',}
        response = self.client.post(self.url, data=data)
        user = auth.get_user(self.client)

        self.assertNotEqual(response.status_code, 302)
        assert (not user.is_authenticated())

        data = {'password': 'test', }
        response = self.client.post(self.url, data=data)
        user = auth.get_user(self.client)

        self.assertNotEqual(response.status_code, 302)
        assert (not user.is_authenticated())

