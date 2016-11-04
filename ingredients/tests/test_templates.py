"""
Test suite for templates.
"""

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from utilities.mock_db import logged_in_client
from ingredients.models import Ingredient


class IngredientDetailTemplateTests(TestCase):
    """
    Test suite to ensure that ingredient_detail template renders correctly.
    """

    def setUp(self):
        self.client = Client()
        self.logged = logged_in_client()
        self.i = Ingredient.objects.create(name='test', type='Fruit',
                                           description='test')
        self.url = reverse('ingredients:ingredient_detail', args=[self.i.slug])

    def test_correct_template_used(self):
        """ Ensures that a correct template is used for a view. """

        response = self.client.get(self.url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'ingredients/ingredient_detail.html')

    def test_template_shows_correct_info(self):
        """
        Ensures that the ingredient_detail template shows all required info.
        """

        response = self.client.get(self.url)

        self.assertContains(response, self.i.name)
        self.assertContains(response, self.i.description)
        self.assertContains(response, self.i.type)
