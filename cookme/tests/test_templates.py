"""
Test suite to ensure that templates show essential information.

These tests are not supposed to test every little bit of it, but just the
essential parts which would be present no matter what.
"""

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from recipes.models import Recipe


class HomePageTests(TestCase):
    """
    Test suite to ensure that home page contains all the necessary elements,
    never mind how they appear (i.e., some elements, e.g. forms or links need
    to be on front page despite the formatting).
    """

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test', password='test')
        self.url = reverse('home')

    def test_search_bar_exists(self):
        """ Ensures that the search bar is on the front page. """

        response = self.client.get(self.url)
        element = f'<form action="{self.url}" method="post" id="search-bar">'

        # Can't make assertContains recognize the form for some reason,
        # even when copying directly from html source on chrome...
        self.assertIn(element, str(response.content))

    def test_popular_shown(self):
        """
        Ensures that the most popular recipes are shown on the front page.
        """

        r1 = Recipe.objects.create(author=self.user, title='test', views=1)
        Recipe.objects.create(author=self.user, title='test2', views=2)
        Recipe.objects.create(author=self.user, title='test3', views=3)
        Recipe.objects.create(author=self.user, title='test4', views=4)
        r5 = Recipe.objects.create(author=self.user, title='test5', views=5)
        expected = f'<h3>{r5.title}</h3>'
        should_not_be = f'<h3>{r1.title}</h3>'
        response = self.client.get(self.url)

        self.assertContains(response, expected, html=True)
        self.assertNotContains(response, should_not_be, html=True)

    def test_popular_not_shown_with_no_recipes(self):
        """
        Ensures that with no recipes, no 'popular' category is shown on the
        front page.
        """

        should_not_be = '<h2>Popular</h2>'
        response = self.client.get(self.url)

        self.assertNotContains(response, should_not_be, html=True)

    def test_most_recent_recipes(self):
        """
        Ensures that the most recent recipes are shown on the front page.
        """

        r1 = Recipe.objects.create(author=self.user, title='test', views=1)
        Recipe.objects.create(author=self.user, title='test2', views=2)
        Recipe.objects.create(author=self.user, title='test3', views=3)
        Recipe.objects.create(author=self.user, title='test4', views=4)
        r5 = Recipe.objects.create(author=self.user, title='test5', views=5)
        expected = f'<h3>{r5.title}</h3>'
        should_not_be = f'<h3>{r1.title}</h3>'
        response = self.client.get(self.url)

        self.assertContains(response, expected, html=True)
        self.assertNotContains(response, should_not_be, html=True)

    def test_recent_not_shown_with_no_recipes(self):
        """
        Ensures that with no recipes, no 'recent' category is shown on the
        front page.
        """

        should_not_be = '<h2>Recent</h2>'
        response = self.client.get(self.url)

        self.assertNotContains(response, should_not_be, html=True)

    def test_new_additions(self):
        """
        Ensures that the most recent recipes are shown on the front page.
        """

        user2 = User.objects.create_user(username='test2', password='test')
        r1 = Recipe.objects.create(author=user2, title='test', views=1)
        Recipe.objects.create(author=user2, title='test2', views=2)
        Recipe.objects.create(author=user2, title='test3', views=3)
        Recipe.objects.create(author=user2, title='test4', views=4)
        Recipe.objects.create(author=user2, title='test5', views=5)
        r6 = Recipe.objects.create(author=self.user, title='test6', views=1)
        expected = f'<h3>{r6.title}</h3>'
        should_not_be = f'<h3>{r1.title}</h3>'
        response = self.client.get(self.url)

        self.assertContains(response, expected, html=True)
        self.assertNotContains(response, should_not_be, html=True)

    def test_new_additions_no_recipe(self):
        """
        Ensures that with no recipes, no 'recent' category is shown on the
        front page.
        """

        should_not_be = '<h2>Your new additions</h2>'
        response = self.client.get(self.url)

        self.assertNotContains(response, should_not_be, html=True)


class RegisterTests(TestCase):
    """ Test suite to ensure register template shows essential information. """

    def setUp(self):
        self.client = Client()
        self.url = reverse('register')

    def test_registered_user_invalid_data(self):
        """
        Ensures invalid registration data is not accepted.

        Note that as the project uses Django's inbuilt authentication system, it
        should not fail. However, if at some point a 3rd party plugin were to be
        installed/developed, it should pass these tests, too.
        """

        data = {'username': 'test', 'password1': 'test', 'password2': 'test'}
        response = self.client.post(self.url, data=data)

        self.assertContains(
            response, 'The password is too similar to the username.')
        self.assertContains(
            response, 'This password is too short. It must contain at least 8 '
                      'characters.')
        self.assertContains(
            response, 'This password is too common.')

    def test_all_fields_missing(self):
        """ Ensures missing input is caught. """

        data = dict()
        response = self.client.post(self.url, data=data)

        self.assertContains(response, 'This field is required.')

    def test_username_field_missing(self):
        """ Ensures missing username input is caught. """

        data = {'password1': 'test', 'password2': 'test'}
        response = self.client.post(self.url, data=data)

        self.assertContains(response, 'This field is required.')

    def test_password1_field_missing(self):
        """ Ensures missing password1 input is caught. """

        data = {'username': 'test', 'password2': 'test'}
        response = self.client.post(self.url, data=data)

        self.assertContains(response, 'This field is required.')

    def test_password2_field_missing(self):
        """ Ensures missing password2 input is caught. """

        data = {'username': 'test', 'password1': 'test'}
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

        Note: do not forget that login page redirects to the previous page.
        """

        response = self.client.get(self.url)
        expected_html = f'<a href={self.url}?next={self.url}>Register</a>'

        self.assertNotContains(response, expected_html, html=True)

    def test_register_shown(self):
        """
        Ensures that register link is shown in other views.

        Note: do not forget that login page redirects to the previous page.
        """

        url = reverse('recipes:recipes')
        response = self.client.get(url)
        expected_html = f'<a href={self.url}?next={url}>Register</a>'

        self.assertContains(response, expected_html, html=True)


class LoginTests(TestCase):
    """ Test suite to ensure that login templates show correct info. """

    def setUp(self):
        self.client = Client()
        self.url = reverse('login')

    def test_login_not_shown(self):
        """
        Ensures that login link is not shown when user is in login view.

        Note: do not forget that login page redirects to the previous page.
        """

        response = self.client.get(self.url)
        expected_html = f'<a href={self.url}?next={self.url}>Login</a>'

        self.assertNotContains(response, expected_html, html=True)

    def test_login_shown(self):
        """
        Ensures that login link is shown in other views.

        Note: do not forget that login page redirects to the previous page.
        """

        url = reverse('recipes:recipes')
        response = self.client.get(url)
        expected_html = f'<a href={self.url}?next={url}>Login</a>'

        self.assertContains(response, expected_html, html=True)
