from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from ingredients.models import Ingredient
from utilities.mock_db import (
    logged_in_client, populate_recipes, populate_ingredients,
)


class IngredientDetailTemplateTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.logged = logged_in_client()
        self.i = Ingredient.objects.create(name='test', type='Fruit', description='test')
        self.url = reverse('ingredients:ingredient_detail', args=[self.i.slug])

    def test_correct_template_used(self):
        response = self.client.get(self.url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'ingredients/ingredient_detail.html')

    def test_template_shows_correct_info(self):
        response = self.client.get(self.url)

        self.assertContains(response, self.i.name)
        self.assertContains(response, self.i.description)
        self.assertContains(response, self.i.type)

    def test_template_shows_recipes(self):
        meat = populate_ingredients()[0]
        meat_recipe = populate_recipes()[0]
        url = reverse('ingredients:ingredient_detail', args=[meat.slug])

        response = self.client.get(url)

        self.assertContains(response, meat.name)
        self.assertContains(response, meat_recipe.title)

    def test_template_no_recipe(self):
        expected_html = '<p>There are no recipes. Why not be the first one to'

        response = self.client.get(self.url)

        self.assertContains(response, self.i.name)
        self.assertContains(response, expected_html)

    def test_no_such_ingredient(self):
        url = reverse('ingredients:ingredient_detail', args=['non-existent'])

        response = self.client.get(url)

        self.assertEquals(response.status_code, 404)
