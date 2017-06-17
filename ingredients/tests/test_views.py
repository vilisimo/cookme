from http import HTTPStatus

from django.contrib.auth.models import User
from django.core.urlresolvers import resolve, reverse
from django.test import TestCase
from django.test.client import Client

from ingredients.models import Ingredient, Unit
from ingredients.views import ingredient_detail
from recipes.models import Recipe, RecipeIngredient
from utilities.mock_db import logged_in_client


class IngredientDetailViewsURLsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.logged = logged_in_client()
        self.i = Ingredient.objects.create(name='test', type='Fruit', description='test')
        self.url = reverse('ingredients:ingredient_detail', kwargs={'slug': self.i.slug})

    def test_URL_resolves_to_correct_view(self):
        view = resolve('/ingredients/' + self.i.slug + '/')

        self.assertEqual(view.func, ingredient_detail)
        self.assertEqual(view.view_name, 'ingredients:ingredient_detail')

    def test_access_for_all(self):
        response = self.client.get(self.url)
        response2 = self.logged.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response2.status_code, HTTPStatus.OK)

    def test_no_ingredient_404(self):
        Ingredient.objects.all().delete()

        response = self.logged.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_ingredient_similar_name_exact_match_shown(self):
        user = User.objects.create_user(username='test', password='test')
        unit = Unit.objects.create(name='Gram', abbrev='g')
        i2 = Ingredient.objects.create(name='test2', type='Fruit', description='test')
        r = Recipe.objects.create(author=user, title='test')
        r2 = Recipe.objects.create(author=user, title='test2')
        RecipeIngredient.objects.create(recipe=r, ingredient=self.i, unit=unit, quantity=1)
        RecipeIngredient.objects.create(recipe=r2, ingredient=i2, unit=unit, quantity=1)

        response = self.client.get(self.url)
        recipes = response.context['recipes']

        self.assertNotIn(r2, recipes)
