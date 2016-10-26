"""
Test suite for views, urls.
"""

from django.core.urlresolvers import resolve, reverse
from django.test import TestCase
from django.test.client import Client

from fridge.tests.test_views import logged_in_client
from ingredients.models import Ingredient
from ingredients.views import ingredient_detail


class IngredientDetailViewsURLsTests(TestCase):
    """ Test suite to ensure that ingredient_detail view works correctly. """

    def setUp(self):
        self.client = Client()
        self.logged = logged_in_client()
        self.i = Ingredient.objects.create(name='test', type='Fruit',
                                           description='test')
        self.url = reverse('ingredients:ingredient_detail',
                           kwargs={'slug':self.i.slug})

    def test_URL_resolves_to_correct_view(self):
        """ Ensures that ingredient's URL resolves to correct view. """

        view = resolve('/ingredients/' + self.i.slug + '/')

        self.assertEqual(view.func, ingredient_detail)

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




