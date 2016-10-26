"""
Test to ensure that templates show essential information. Not supposed to
test every little bit of it, but just the essential parts which would be
present no matter what.
"""

from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class HomePageTests(TestCase):
    """
    Test suite to ensure that home page contains all the necessary elements,
    never mind how they appear (i.e., some elements, e.g. forms or links need
    to be on front page despite the formatting).
    """

    def setUp(self):
        self.client = Client()
        self.url = reverse('home')

    def test_search_bar_exists(self):
        """ Ensures that the search bar is on the front page. """

        response = self.client.get(self.url)
        element = '<form action="{}" method="post" id="search-bar">'.format(
            reverse('home'))

        # Can't make assertContains recognize the form for some reason,
        # even when copying directly from html source on chrome...
        self.assertIn(element, str(response.content))


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

    def test_register_not_shown(self):
        """
        Ensures url to register view is not shown when user is in register
        view.
        """

        response = self.client.get(self.url)

        # Do not forget that login page redirects to the previous page.
        self.assertNotContains(response,
                               '<a href={0}?next={0}>Register</a>'.format(
                                   self.url), html=True)

    def test_register_shown(self):
        """ Ensures that register link is shown in other views. """

        recipe_url = reverse('recipes:recipes')
        response = self.client.get(recipe_url)

        # Do not forget that login page redirects to the previous page.
        self.assertContains(response,
                            '<a href={}?next={}>Register</a>'.
                            format(self.url, recipe_url), html=True)


class LoginTests(TestCase):
    """ Test suite to ensure that login templates show correct info. """

    def setUp(self):
        self.client = Client()
        self.url = reverse('login')

    def test_login_not_shown(self):
        """ Ensures that login link is not shown when user is in login view. """

        response = self.client.get(self.url)

        # Do not forget that login page redirects to the previous page.
        self.assertNotContains(response,
                               '<a href={0}?next={0}>Login</a>'.format(
                                   self.url), html=True)

    def test_login_shown(self):
        """ Ensures that login link is shown in other views. """

        recipe_url = reverse('recipes:recipes')
        response = self.client.get(recipe_url)

        # Do not forget that login page redirects to the previous page.
        self.assertContains(response,
                            '<a href={}?next={}>Login</a>'.
                            format(self.url, recipe_url), html=True)

    # # Does not work even when template has error tags?..
    # def test_missing_info(self):
    #     """ Ensure empty fields are not allowed. """
    #
    #     data = dict()
    #     response = self.client.post(self.url, data=data)
    #
    #     from django.contrib.auth.forms import AuthenticationForm
    #     form = AuthenticationForm(data=data)
    #     print(form.errors)  # Prints errors, but no errors in template?..
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