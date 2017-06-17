import urllib.parse
from http import HTTPStatus

from django.contrib import auth
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, resolve
from django.test import TestCase
from django.test.client import Client

from cookme.views import home, register
from recipes.models import Recipe
from utilities.search_helpers import encode


class HomePageTests(TestCase):
    """ Ensures that home page functions properly. """

    def setUp(self):
        self.url = reverse('home')
        self.user = User.objects.create_user(username='test', password='test')
        self.logged = Client()
        self.logged.login(username='test', password='test')

    def test_correct_root_url_resolves_to_home_function(self):
        view = resolve('/')

        self.assertEqual(view.view_name, 'home')
        self.assertEqual(view.func, home)

    def test_anonymous_does_not_see_fridge(self):
        response = Client().get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertNotContains(response, 'Fridge')

    def test_logged_sees_fridge(self):
        response = self.logged.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Fridge')

    def test_most_popular_shown_on_front_page(self):
        r1, *_, r5 = self.create_recipes_asc_views(repeat=5)

        response = Client().get(self.url)
        recipes = response.context['most_popular']

        self.assertIn(r5, recipes)
        self.assertNotIn(r1, recipes)
        self.assertEquals(len(recipes), 4)

    def test_most_popular_not_shown(self):
        response = Client().get(self.url)
        recipes = response.context['most_popular']

        self.assertFalse(recipes)

    def test_most_popular_less_than_four(self):
        r1, r2, r3 = self.create_recipes_asc_views(repeat=3)

        response = Client().get(self.url)
        recipes = response.context['most_popular']

        self.assertEquals([r3, r2, r1], list(recipes))

    def test_recipes_equal_views_oldest_first(self):
        r1, r2, r3 = self.create_recipes_const_views(repeat=3, views=1)

        response = Client().get(self.url)
        recipes = response.context['most_popular']

        self.assertEquals([r1, r2, r3], list(recipes))

    def test_recipes_most_recent_shown(self):
        old, *_, recent = self.create_recipes_asc_views(repeat=5)

        response = Client().get(self.url)
        recipes = response.context['most_recent']

        self.assertIn(recent, recipes)
        self.assertNotIn(old, recipes)
        self.assertEqual(len(recipes), 4)

    def test_recent_additions_by_user(self):
        user2 = User.objects.create_user(username='test2', password='test')
        other_user_old = Recipe.objects.create(author=user2, title='test')
        *_, new_addition = self.create_recipes_asc_views(repeat=4)

        response = self.logged.get(self.url)
        recipes = response.context['user_additions']

        self.assertIn(new_addition, recipes)
        self.assertNotIn(other_user_old, recipes)
        self.assertEqual(len(recipes), 4)

    def test_recent_additions_not_shown_for_anonymous(self):
        with self.assertRaises(KeyError):
            response = Client().get(self.url)
            recipes = response.context['user_additions']

            self.assertFalse(recipes)

    def test_recent_additions_by_user_order_descending(self):
        old, *_, new = self.create_recipes_asc_views(repeat=5)

        response = self.logged.get(self.url)
        recipes = response.context['user_additions']

        self.assertIn(new, recipes)
        self.assertNotIn(old, recipes)
        self.assertEqual(len(recipes), 4)

    # Helper functions
    def create_recipes_asc_views(self, repeat):
        recipes = []
        for views in range(repeat):
            title = f'test{views}'
            recipes.append(Recipe.objects.create(author=self.user, title=title,
                                                 views=views))
        return recipes

    def create_recipes_const_views(self, repeat, views):
        recipes = []
        for nr in range(repeat):
            title = f'test{nr}'
            recipes.append(Recipe.objects.create(author=self.user, title=title,
                                                 views=views))
        return recipes


class SearchFunctionTests(TestCase):

    def setUp(self):
        self.url = reverse('home')
        self.client = Client()

    def test_search_form_response_ok(self):
        data = {'q': 'valid inquiry that should not throw errors'}

        response = self.client.post(path=self.url, data=data)

        self.assertEqual(response.status_code, 302)

    def test_search_form_redirection_url_ok(self):
        query = encode("secret grandma's ingredient")
        query_utf_encoded = urllib.parse.quote_plus(query)
        data = {'q': query}
        expected_url = reverse('search:search_results') + '?q=' + query_utf_encoded

        response = self.client.post(self.url, data)

        self.assertRedirects(response, expected_url=expected_url)

    def test_search_form_redirection_url_ok_utf_searchphrase(self):
        query = encode("šecret grandma's ingredient")
        query_utf_encoded = urllib.parse.quote_plus(query)
        data = {'q': query}
        expected_url = reverse('search:search_results') + '?q=' + query_utf_encoded

        response = self.client.post(self.url, data)

        self.assertRedirects(response, expected_url=expected_url)


class RegisterViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('register')
        self.data = {
            'username': 'ElaborateUsername',
            'password1': 'VerySecretPassword',
            'password2': 'VerySecretPassword'
        }

    def test_correct_url_mapped_to_view(self):
        view = resolve('/accounts/register/')

        self.assertEqual(view.view_name, 'register')
        self.assertEqual(view.func, register)

    def test_can_access_register_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_has_register_form(self):
        response = self.client.get(self.url)

        self.assertTrue(response.context['form'])

    def test_registered_user_redirected(self):
        User.objects.create_user(username='test', password='test')
        client = Client()
        client.login(username='test', password='test')

        response = client.get(self.url)

        self.assertRedirects(response, reverse('home'), status_code=HTTPStatus.FOUND)

    def test_redirect_upon_valid_data(self):
        response = self.client.post(self.url, data=self.data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_user_created_when_data_valid(self):
        self.client.post(self.url, data=self.data)
        user = User.objects.get(username='ElaborateUsername')

        self.assertTrue(user)

    def test_user_logged_in_when_valid_data(self):
        self.client.post(self.url, data=self.data)
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated())

        # Just to make sure we are really logged in.
        response = self.client.get(reverse('fridge:fridge_detail'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_username_exists(self):
        User.objects.create_user(username=self.data['username'],
                                 password=self.data['password1'])

        response = self.client.post(self.url, data=self.data)

        self.assertTrue(response.status_code != HTTPStatus.FOUND)


class LoginTests(TestCase):
    """
    Test suite to ensure login works correctly. Although at the moment
    Django's login functionality is used, it may change in the future.
    """

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.url = reverse('login')
        self.client = Client()

    def test_invalid_data(self):
        data = {
            'username': 'test',
            'password': 'testing',
        }

        response = self.client.post(self.url, data=data)
        user = auth.get_user(self.client)

        self.assertNotEqual(response.status_code, HTTPStatus.FOUND)
        self.assertFalse(user.is_authenticated())

    def test_login_with_valid_data(self):
        data = {
            'username': 'test',
            'password': 'test',
        }

        response = self.client.post(self.url, data=data)
        user = auth.get_user(self.client)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(user.is_authenticated())

    def test_missing_password(self):
        data = {'username': 'test', }

        response = self.client.post(self.url, data=data)
        user = auth.get_user(self.client)

        self.assertNotEqual(response.status_code, HTTPStatus.FOUND)
        self.assertFalse(user.is_authenticated())

    def test_missing_username(self):
        data = {'password': 'test', }

        response = self.client.post(self.url, data=data)
        user = auth.get_user(self.client)

        self.assertNotEqual(response.status_code, HTTPStatus.FOUND)
        self.assertFalse(user.is_authenticated())

