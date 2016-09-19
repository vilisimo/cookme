"""
Test suite for views, urls.
"""


from django.test import TestCase
from django.core.urlresolvers import resolve, reverse
from django.test.client import Client

from fridge.test_views import logged_in_client
from .models import Ingredient
from .views import ingredient_detail


class IngredientDetailViewsURLsTests(TestCase):
    """ Test suite to ensure that ingredient_detail view works correctly. """

    def setUp(self):
        self.client = Client()
        self.logged = logged_in_client()
        self.i = Ingredient.objects.create(name='test', type='Fruit',
                                           description='test')

    def test_URL_resolves_to_correct_view(self):
        """ Ensures that ingredient's URL resolves to correct view. """

        view = resolve('/ingredients/' + self.i.slug + '/')

        self.assertEqual(view.func, ingredient_detail)

    def test_user_access(self):
        """ Ensures that all users can access ingredient details. """

        response = self.client.get(reverse('ingredients:ingredient_detail',
                                   args=[self.i.slug]))
        response2 = self.logged.get(reverse('ingredients:ingredient_detail',
                                    args=[self.i.slug]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response2.status_code, 200)

    def test_no_ingredient_404(self):
        """
        Ensures that a user is shown 404 error when there is no ingredient.
        """

        Ingredient.objects.all().delete()

        response = self.logged.get(reverse('ingredients:ingredient_detail',
                                   args=[self.i.slug]))

        self.assertEqual(response.status_code, 404)




