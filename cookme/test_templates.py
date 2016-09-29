"""
Test to ensure that templates show essential information. Not supposed to
test every little bit of it, but just the essential parts which would be
present no matter what.
"""

from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class RegisterTests(TestCase):
    """ Test suite to ensure register template shows essential infomration. """

    def setUp(self):
        self.client = Client()
        self.url = reverse('register')

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

    def test_fields_missing(self):
        """ Ensures missing fields are caught. """

        data = dict()
        response = self.client.post(self.url, data=data)

        self.assertContains(response, 'This field is required.')

        data['username'] = 'test'
        response = self.client.post(self.url, data=data)

        self.assertContains(response, 'This field is required.')

        data['password1'] = 'test'
        response = self.client.post(self.url, data=data)

        self.assertContains(response, 'This field is required.')

        data = {'username': 'test', 'password2': 'test'}
        response = self.client.post(self.url, data=data)

        self.assertContains(response, 'This field is required.')

    def test_register_user_already_exists(self):
        """ Ensures duplicate accounts cannot be created. """

        User.objects.create_user(username='test', password='test')
        data = {'username': 'test', 'password1': 'test', 'password2': 'test'}
        response = self.client.post(self.url, data=data)

        self.assertContains(
            response, 'A user with that username already exists.')


class LoginTests(TestCase):
    """ Test suite to ensure that login templates show correct info. """

    def setUp(self):
        self.client = Client()
        self.url = reverse('login')

    # # Does not work even when template has error tags?..
    # def test_missing_info(self):
    #     """ Ensure empty fields are not allowed. """
    #
    #     data = dict()
    #     response = self.client.post(self.url, data=data)
    #
    #     from django.contrib.auth.forms import AuthenticationForm
    #     form = AuthenticationForm(data=data)
    #     print(form.errors)  # Prints errors, but no erros in template?..
    #
    #     self.assertContains(response, 'This field is required.')
    #
    #     data['username'] = 'test'
    #     response = self.client.post(self.url, data=data)
    #
    #     self.assertContains(response, 'This field is required.')
    #
    #     data = {'password': 'test'}
    #     response = self.client.post(self.url, data=data)
    #
    #     self.assertContains(response, 'This field is required.')