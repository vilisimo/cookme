from django.test import TestCase

from .models import Ingredient

from django.core.urlresolvers import reverse, resolve


class IngredientTestCase(TestCase):
    def setUp(self):
        Ingredient.objects.create(name='Meat', type='Meat')

    def test_str_representation(self):
        ingredient = Ingredient.objects.get(name='Meat')
        self.assertEqual(str(ingredient), ingredient.name)


class UrlTestCase(TestCase):
    def test_recipes_url(self):
        resolver = resolve('/recipes/')
        self.assertEqual(resolver.view_name, 'recipes')


class ViewsTestCase(TestCase):
    def test_recipes_view(self):
        response = self.client.get(reverse('recipes'))
        self.assertEqual(response.status_code, 200)

        # More tests are needed
