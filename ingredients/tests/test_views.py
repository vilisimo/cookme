"""
Test suite for views, urls.
"""

from django.core.urlresolvers import resolve, reverse
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

from utilities.mock_db import logged_in_client
from ingredients.models import Ingredient, Unit
from ingredients.views import ingredient_detail
from recipes.models import Recipe, RecipeIngredient


class IngredientDetailViewsURLsTests(TestCase):
    """
    Test suite to ensure that ingredient_detail view can be accessed by all
    users.
    """

    def setUp(self):
        self.client = Client()
        self.logged = logged_in_client()
        self.i = Ingredient.objects.create(name='test', type='Fruit',
                                           description='test')
        self.url = reverse('ingredients:ingredient_detail',
                           kwargs={'slug': self.i.slug})

    def test_URL_resolves_to_correct_view(self):
        """ Ensures that ingredient's URL resolves to correct view. """

        view = resolve('/ingredients/' + self.i.slug + '/')

        self.assertEqual(view.func, ingredient_detail)
        self.assertEqual(view.view_name, 'ingredients:ingredient_detail')

    def test_user_access(self):
        """ Ensures that all users can access ingredient details. """

        response = self.client.get(self.url)
        response2 = self.logged.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response2.status_code, 200)

    def test_no_ingredient_404(self):
        """
        Ensures that a user is shown 404 error when there is no ingredient.
        """

        Ingredient.objects.all().delete()
        response = self.logged.get(self.url)

        self.assertEqual(response.status_code, 404)

    def test_ingredient_similar_name(self):
        """
        Ensures that when an ingredient has a similar name to another one (
        e.g., Lemon and Lemongrass), only the exact match is shown.
        """

        u = User.objects.create_user(username='test', password='test')
        unit = Unit.objects.create(name='Gram', abbrev='g')
        i2 = Ingredient.objects.create(name='test2', type='Fruit',
                                       description='test')
        r = Recipe.objects.create(author=u, title='test')
        RecipeIngredient.objects.create(recipe=r, ingredient=self.i,
                                        unit=unit, quantity=1)
        r2 = Recipe.objects.create(author=u, title='test2')
        RecipeIngredient.objects.create(recipe=r2, ingredient=i2,
                                        unit=unit, quantity=1)

        response = self.client.get(self.url)
        recipes = response.context['recipes']

        self.assertNotIn(r2, recipes)






