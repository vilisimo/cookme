from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from recipes.models import Recipe


class HomePageTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test', password='test')
        self.url = reverse('home')

    def test_search_bar_on_front_page(self):
        element = f'<form action="{self.url}" method="post" id="search-bar">'

        response = self.client.get(self.url)

        # assertContains does not recognize the form for some reason
        self.assertIn(element, str(response.content))

    def test_most_popular_recipes_shown(self):
        least_pop, *_, most_pop = recipes_asc_views(count=5, user=self.user)
        expected = f'<h3>{most_pop.title}</h3>'
        should_not_be = f'<h3>{least_pop.title}</h3>'

        response = self.client.get(self.url)

        self.assertContains(response, expected, html=True)
        self.assertNotContains(response, should_not_be, html=True)

    def test_most_popular_category_not_shown_with_no_recipes(self):
        should_not_be = '<h2>Popular</h2>'

        response = self.client.get(self.url)

        self.assertNotContains(response, should_not_be, html=True)

    def test_most_recent_recipes_shown(self):
        oldest, *_, newest = recipes_asc_views(count=5, user=self.user)
        expected = f'<h3>{newest.title}</h3>'
        should_not_be = f'<h3>{oldest.title}</h3>'

        response = self.client.get(self.url)

        self.assertContains(response, expected, html=True)
        self.assertNotContains(response, should_not_be, html=True)

    def test_most_recent_not_shown_with_no_recipes(self):
        should_not_be = '<h2>Recent</h2>'

        response = self.client.get(self.url)

        self.assertNotContains(response, should_not_be, html=True)

    def test_new_additions_shown_on_front_page(self):
        user2 = User.objects.create_user(username='test2', password='test')
        old, *_ = recipes_asc_views(count=5, user=user2)
        new = Recipe.objects.create(author=self.user, title='test6', views=1)
        expected = f'<h3>{new.title}</h3>'
        should_not_be = f'<h3>{old.title}</h3>'

        response = self.client.get(self.url)

        self.assertContains(response, expected, html=True)
        self.assertNotContains(response, should_not_be, html=True)

    def test_recent_additions_not_shown_with_no_recipes(self):
        should_not_be = '<h2>Your new additions</h2>'

        response = self.client.get(self.url)

        self.assertNotContains(response, should_not_be, html=True)


# Helper functions
def recipes_asc_views(count, user):
    recipes = []
    for views in range(count):
        title = f'test{views}'
        recipes.append(Recipe.objects.create(author=user, title=title, views=views))
    return recipes


class RegisterTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('register')

    def test_registered_user_invalid_data(self):
        data = {'username': 'test', 'password1': 'test', 'password2': 'test'}

        response = self.client.post(self.url, data=data)

        self.assertContains(response, 'This password is too common.')
        self.assertContains(response, 'The password is too similar to the username.')
        self.assertContains(response, 'This password is too short. It must contain at '
                                      'least 8 characters.')

    def test_all_fields_missing(self):
        response = self.client.post(self.url, data=(dict()))

        self.assertContains(response, 'This field is required.')

    def test_username_field_missing(self):
        data = {'password1': 'test', 'password2': 'test'}

        response = self.client.post(self.url, data=data)

        self.assertContains(response, 'This field is required.')

    def test_password1_field_missing(self):
        data = {'username': 'test', 'password2': 'test'}

        response = self.client.post(self.url, data=data)

        self.assertContains(response, 'This field is required.')

    def test_password2_field_missing(self):
        data = {'username': 'test', 'password1': 'test'}

        response = self.client.post(self.url, data=data)

        self.assertContains(response, 'This field is required.')

    def test_register_user_already_exists(self):
        User.objects.create_user(username='test', password='test')
        data = {'username': 'test', 'password1': 'test', 'password2': 'test'}

        response = self.client.post(self.url, data=data)

        self.assertContains(response, 'A user with that username already exists.')

    def test_register_not_shown_in_register_view(self):
        expected_html = f'<a href={self.url}?next={self.url}>Register</a>'

        response = self.client.get(self.url)

        self.assertNotContains(response, expected_html, html=True)

    def test_register_shown_in_other_views(self):
        url = reverse('recipes:recipes')
        expected_html = f'<a href={self.url}?next={url}>Register</a>'

        response = self.client.get(url)

        self.assertContains(response, expected_html, html=True)


class LoginTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('login')

    def test_login_not_shown_in_login_view(self):
        expected_html = f'<a href={self.url}?next={self.url}>Login</a>'

        response = self.client.get(self.url)

        self.assertNotContains(response, expected_html, html=True)

    def test_login_shown_in_other_views(self):
        url = reverse('recipes:recipes')
        expected_html = f'<a href={self.url}?next={url}>Login</a>'

        response = self.client.get(url)

        self.assertContains(response, expected_html, html=True)
