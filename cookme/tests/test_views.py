"""
Tests to ensure everything in cookme.views works correctly.
"""

import urllib.parse

from django.contrib import auth
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, resolve
from django.test import TestCase
from django.test.client import Client

from cookme.views import home, register
from utilities.search_helpers import encode
from recipes.models import Recipe


class HomePageTests(TestCase):
    """ Test suite to ensure that home page functions properly. """

    def setUp(self):
        self.url = reverse('home')
        self.user = User.objects.create_user(username='test', password='test')
        self.logged = Client()
        self.logged.login(username='test', password='test')

    def test_correct_root_url_resolves_to_home_function(self):
        """
        Test suite to ensure that the root URL is mapped to a correct view.
        """

        view = resolve('/')

        self.assertEqual(view.view_name, 'home')
        self.assertEqual(view.func, home)

    def test_anonymous_visit(self):
        """ Ensures anonymous users do not see a link to a fridge. """

        response = Client().get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Fridge')

    def test_logged_visit(self):
        """ Ensures that logged in user sees a fridge. """

        response = self.logged.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Fridge')

    def test_most_popular_exist(self):
        """
        Ensures that the most popular recipes are shown on the front page.
        There should be 4 most popular recipes shown on the front page.
        """

        r1 = Recipe.objects.create(author=self.user, title='test', views=1)
        Recipe.objects.create(author=self.user, title='test2', views=2)
        Recipe.objects.create(author=self.user, title='test3', views=3)
        Recipe.objects.create(author=self.user, title='test4', views=4)
        r5 = Recipe.objects.create(author=self.user, title='test5', views=5)

        response = Client().get(self.url)
        recipes = response.context['most_popular']

        self.assertIn(r5, recipes)
        self.assertNotIn(r1, recipes)
        self.assertEquals(len(recipes), 4)

    def test_most_popular_do_not_exist(self):
        """
        Ensures that when there are no most popular recipes, no recipes are
        passed to response's context.
        """

        response = Client().get(self.url)
        recipes = response.context['most_popular']

        self.assertFalse(recipes)

    def test_most_popular_less_than_four(self):
        """
        Ensures that when there are less than four recipes, all of them are
        shown.
        """

        r1 = Recipe.objects.create(author=self.user, title='test', views=1)
        r2 = Recipe.objects.create(author=self.user, title='test2', views=2)
        r3 = Recipe.objects.create(author=self.user, title='test3', views=3)

        response = Client().get(self.url)
        recipes = response.context['most_popular']

        self.assertEquals([r3, r2, r1], list(recipes))

    def test_recipes_equal_views(self):
        """
        Ensures that the oldest recipes are shown first if all most popular
        recipes have the same amount of views.
        """

        r1 = Recipe.objects.create(author=self.user, title='test', views=1)
        r2 = Recipe.objects.create(author=self.user, title='test2', views=1)
        r3 = Recipe.objects.create(author=self.user, title='test3', views=1)

        response = Client().get(self.url)
        recipes = response.context['most_popular']

        self.assertEquals([r1, r2, r3], list(recipes))

    def test_recipes_most_recent(self):
        """
        Ensures that the most recent recipes are shown on the front page.
        """

        r1 = Recipe.objects.create(author=self.user, title='test')
        Recipe.objects.create(author=self.user, title='test2')
        Recipe.objects.create(author=self.user, title='test3')
        Recipe.objects.create(author=self.user, title='test4')
        r5 = Recipe.objects.create(author=self.user, title='test5')

        response = Client().get(self.url)
        recipes = response.context['most_recent']

        self.assertIn(r5, recipes)
        self.assertNotIn(r1, recipes)
        self.assertEqual(len(recipes), 4)

    def test_recent_additions_by_user(self):
        """
        Ensures that the front page is passed recipes that a user has 
        recently added.
        """

        user2 = User.objects.create_user(username='test2', password='test')
        r1 = Recipe.objects.create(author=user2, title='test')
        Recipe.objects.create(author=self.user, title='test2')
        Recipe.objects.create(author=self.user, title='test3')
        Recipe.objects.create(author=self.user, title='test4')
        r5 = Recipe.objects.create(author=self.user, title='test5')

        response = self.logged.get(self.url)
        recipes = response.context['user_additions']

        self.assertIn(r5, recipes)
        self.assertNotIn(r1, recipes)
        self.assertEqual(len(recipes), 4)

    def test_recent_additions_by_user_anonymous_onlooker(self):
        """
        Ensures that recent additions are not shown for users that are not
        logged in.
        """

        with self.assertRaises(KeyError):
            response = Client().get(self.url)
            recipes = response.context['user_additions']

            self.assertFalse(recipes)

    def test_recent_additions_by_user_order_descending(self):
        """
        Ensures that the front page is passed recipes that a user has
        recently added AND that they are ordered from newest to oldest.
        """

        r1 = Recipe.objects.create(author=self.user, title='test')
        Recipe.objects.create(author=self.user, title='test2')
        Recipe.objects.create(author=self.user, title='test3')
        Recipe.objects.create(author=self.user, title='test4')
        r5 = Recipe.objects.create(author=self.user, title='test5')

        response = self.logged.get(self.url)
        recipes = response.context['user_additions']

        self.assertIn(r5, recipes)
        self.assertNotIn(r1, recipes)
        self.assertEqual(len(recipes), 4)


class SearchFunctionTests(TestCase):
    """
    Test suite to ensure that search functionality is performing as expected.
    """

    def setUp(self):
        self.url = reverse('home')
        self.client = Client()

    def test_search_form_response_ok(self):
        """
        Ensures that inputting the correct info in search bar search_results in
        correct response status (302 - redirects to results page).
        """

        data = {'q': 'multiple words and then some'}
        response = self.client.post(path=self.url, data=data)

        self.assertEqual(response.status_code, 302)

    def test_search_form_redirection_url_ok(self):
        """
        Ensures that inputting the correct info in search bar will redirect to
        the correct view.
        """

        query = "secret grandma's ingredient"
        query = encode(query)
        query_utf_encoded = urllib.parse.quote_plus(query)
        data = {'q': query}
        response = self.client.post(self.url, data)
        url = reverse('search:search_results') + '?q=' + query_utf_encoded

        self.assertRedirects(response, expected_url=url)

    def test_search_form_redirection_url_ok_utf(self):
        """
        Ensures that inputting the correct info in search bar will
        redirect to the correct view, even when UTF-8 char is used.
        """

        query = "šecret grandma's ingredient"
        query = encode(query)
        query_utf_encoded = urllib.parse.quote_plus(query)
        data = {'q': query}
        response = self.client.post(self.url, data)
        url = reverse('search:search_results') + '?q=' + query_utf_encoded

        self.assertRedirects(response, expected_url=url)


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
        response = self.client.get(reverse('fridge:fridge_detail'))

        self.assertTrue(user.is_authenticated())
        # Just to make sure we are really logged in.
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
        self.assertFalse(user.is_authenticated())

    def test_valid_data(self):
        """ Ensures that upon submitting valid data, user can log in. """

        data = {
            'username': 'test',
            'password': 'test',
        }

        response = self.client.post(self.url, data=data)
        user = auth.get_user(self.client)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(user.is_authenticated())

    def test_missing_password(self):
        """ Ensure that not filling in password field is not allowed. """

        data = {'username': 'test', }
        response = self.client.post(self.url, data=data)
        user = auth.get_user(self.client)

        self.assertNotEqual(response.status_code, 302)
        self.assertFalse(user.is_authenticated())

    def test_missing_username(self):
        """ Ensure that not filling in username field is not allowed. """

        data = {'password': 'test', }
        response = self.client.post(self.url, data=data)
        user = auth.get_user(self.client)

        self.assertNotEqual(response.status_code, 302)
        self.assertFalse(user.is_authenticated())

