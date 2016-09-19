"""
Test suite for templates.
"""

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from fridge.test_views import logged_in_client
from .models import Ingredient


class IngredientDetailTemplateTests(TestCase):
    """
    Test suite to ensure that ingredient_detail template renders correctly.
    """

    def setUp(self):
        self.client = Client()
        self.logged = logged_in_client()
        self.i = Ingredient.objects.create(name='test', type='Fruit',
                                           description='test')

    def test_template_shows_correct_info(self):
        """
        Ensures that the ingredient_detail template shows all required info.
        """

        response = self.client.get(reverse('ingredients:ingredient_detail',
                                           args=[self.i.slug]))

        self.assertContains(response, self.i.name)
        self.assertContains(response, self.i.description)
        self.assertContains(response, self.i.type)
