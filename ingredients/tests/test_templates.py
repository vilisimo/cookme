"""
Test suite for templates.
"""

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from ingredients.models import Ingredient
from utilities.mock_db import (
    logged_in_client, populate_recipes, populate_ingredients,
)


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

    def test_template_shows_recipes(self):
        """
        Ensures that when an ingredient is used in recipes, those are shown
        on ingredient's page.
        """

        # Clean up: not needed, but serves as a reminder that
        # populate_ingredients() returns 4 ingredients.
        # # Ingredient.objects.all().delete()

        meat = populate_ingredients()[0]
        meatrec = populate_recipes()[0]
        url = reverse('ingredients:ingredient_detail', args=[meat.slug])
        response = self.client.get(url)

        self.assertContains(response, meat.name)
        self.assertContains(response, meatrec.title)

    def test_template_no_recipe(self):
        """
        Ensures that an ingredient is shown, but not its recipes if the
        ingredient is not used in any of them.
        """

        response = self.client.get(self.url)
        expected_html = '<p>There are no recipes. Why not be the first one to'

        self.assertContains(response, self.i.name)
        self.assertContains(response, expected_html)

    def test_no_such_ingredient(self):
        """
        Ensures that when there is no such ingredient, 404 is thrown.
        """

        url = reverse('ingredients:ingredient_detail', args=['non-existent'])
        response = self.client.get(url)

        self.assertEquals(response.status_code, 404)
