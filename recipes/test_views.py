"""
Test suite for views, urls & templates.
"""


from django.test import TestCase

from django.core.urlresolvers import resolve
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


class RecipeViewTests(TestCase):
    """ Test suite to ensure that Recipes view works correctly. """

    def setUp(self):
        self.client = Client()
        self.url = reverse('recipes:recipes')

    def test_recipes_view(self):
        """ Ensures that the recipes view renders correctly. """

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)


class RecipeDetailTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test')
        self.r = Recipe.objects.create(author=self.user, title='test',
                                       description='')
        self.url = reverse('recipes:recipe_detail',
                           kwargs={'slug': self.r.slug})

    def test_recipe_detail_view(self):
        """ Ensures that recipe detail view renders correctly. """

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_recipe_detail_view_context(self):
        """ Test to ensure that the context is passed correct arguments. """

        ingredient = Ingredient.objects.create(name='apple', type='Fruit')
        unit = Unit.objects.create(name='kilogram', abbrev='kg')
        RecipeIngredient.objects.create(recipe=self.r, ingredient=ingredient,
                                        unit=unit, quantity=0.5)

        response = self.client.get(self.url)
        ingredients = RecipeIngredient.objects.filter(recipe=self.r)

        # QuerySets are not equal even if they contain the same values,
        # hence we need to convert them to lists.
        self.assertEqual(list(response.context['ingredients']),
                         list(ingredients))

    def test_non_existent_recipe(self):
        """ Ensures that non-existent recipe throws 404. """

        Recipe.objects.all().delete()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 404)
