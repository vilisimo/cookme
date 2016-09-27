from django.test import TestCase
from django.core.urlresolvers import reverse, resolve
from django.contrib.auth.models import User
from django.test.client import Client

from .views import home, register


###################################
""" Test Views, URLS & Templates"""
###################################


class HomePageTests(TestCase):
    """ Test suite to ensure that home page functions properly. """

    def setUp(self):
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

        response = Client().get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Fridge')

    def test_logged_visit(self):
        """ Test to ensure that logged in user sees the fridge. """

        response = self.logged.get(reverse('home'))

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
        """ Ensures a registered user is redirected from a view. """

        User.objects.create_user(username='test', password='test')
        client = Client()
        client.login(username='test', password='test')
        response = client.get(self.url)

        self.assertRedirects(response, reverse('home'), status_code=302)

    def test_registered_user_invalid_data(self):
        """ Ensures invalid data cannot be posted. """

        data = {'username': 'test', 'password1': 'test', 'password2': 'test'}
        response = self.client.post(self.url, data=data)

        self.assertContains(
            response, 'The password is too similar to the username.')
        self.assertContains(
            response, 'This password is too short. It must contain at least 8 '
                      'characters.')
        self.assertContains(
            response, 'This password is too common.')

    def test_register_user_already_exists(self):
        """ Ensures duplicate accounts cannot be created. """

        User.objects.create_user(username='test', password='test')
        data = {'username': 'test', 'password1': 'test', 'password2': 'test'}
        response = self.client.post(self.url, data=data)

        self.assertContains(
            response, 'A user with that username already exists.')

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

        from django.contrib import auth

        data = {
            'username': 'ElaborateUsername',
            'password1': 'VerySecretPassword',
            'password2': 'VerySecretPassword'
        }
        client = Client()
        client.post(self.url, data=data)
        user = auth.get_user(client)

        assert user.is_authenticated()
        # Just to make sure we are really logged in.
        response = client.get(reverse('fridge:fridge_detail'))
        self.assertEqual(response.status_code, 200)
