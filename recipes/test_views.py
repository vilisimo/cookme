"""
Test suite for views, urls & templates.
"""


from django.test import TestCase

from django.core.urlresolvers import reverse, resolve
from django.contrib.auth.models import User
from django.test.client import Client

from .models import *
from .views import recipes, recipe_detail


class URLTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test')
        self.r = Recipe.objects.create(author=self.user, title='test',
                                       description='')

    def test_recipes_url(self):
        """ Ensures that a user is shown a correct URL for recipes. """

        resolver = resolve('/recipes/')
        self.assertEqual(resolver.view_name, 'recipes:recipes')
        self.assertEqual(resolver.func, recipes)

    def test_recipes_detail_url(self):
        """
        Ensures that a user is shown a correct URL for recipe detail page.
        """

        recipe_path = self.r.slug + '/'
        resolver = resolve('/recipes/' + recipe_path)
        self.assertEqual(resolver.view_name, 'recipes:recipe_detail')
        self.assertEqual(resolver.func, recipe_detail)


class ViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test')
        self.r = Recipe.objects.create(author=self.user, title='test',
                                       description='')

    def test_recipes_view(self):
        """ Ensures that the recipes view renders correctly. """

        url = reverse('recipes:recipes')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_recipe_detail_view(self):
        """ Ensures that recipe detail view renders correctly. """

        url = reverse('recipes:recipe_detail', kwargs={'slug': self.r.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


""" Testing helper functions """


# Function that is currently not used.
class UserDirectoryPathTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test')
        self.r = Recipe.objects.create(author=self.user, title='test')
        self.path = user_directory_path(self.r, 'burbt')

    def test_path(self):
        self.assertEqual(self.path, "user_{0}/{1}".format(self.user.id,
                                                          'burbt'))