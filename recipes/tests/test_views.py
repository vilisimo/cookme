from http import HTTPStatus

from django.core.urlresolvers import resolve
from django.test import TestCase
from django.test.client import Client

from fridge.models import Fridge
from recipes.models import *
from recipes.views import recipes, recipe_detail, add_to_fridge


class URLTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test')
        self.r = Recipe.objects.create(author=self.user, title='test', description='')

    def test_recipes_url_maps_to_correct_view(self):
        resolver = resolve('/recipes/')

        self.assertEqual(resolver.view_name, 'recipes:recipes')
        self.assertEqual(resolver.func, recipes)

    def test_recipes_detail_url_maps_to_correct_view(self):
        recipe_path = self.r.slug + '/'

        resolver = resolve('/recipes/' + recipe_path)

        self.assertEqual(resolver.view_name, 'recipes:recipe_detail')
        self.assertEqual(resolver.func, recipe_detail)


class RecipeViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('recipes:recipes')

    def test_recipes_view_accessible_to_all(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)


class RecipeDetailTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test')
        self.r = Recipe.objects.create(author=self.user, title='test', description='')
        self.url = reverse('recipes:recipe_detail', kwargs={'slug': self.r.slug})

    def test_recipe_detail_view_accessible_to_all(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_recipe_detail_view_context(self):
        ingredient = Ingredient.objects.create(name='apple', type='Fruit')
        unit = Unit.objects.create(name='kilogram', abbrev='kg')
        RecipeIngredient.objects.create(recipe=self.r, ingredient=ingredient, unit=unit,
                                        quantity=0.5)
        ingredients = RecipeIngredient.objects.filter(recipe=self.r)

        response = self.client.get(self.url)

        # QuerySets are not equal even if they contain the same values,
        # hence we need to convert them to lists.
        self.assertEqual(list(response.context['ingredients']), list(ingredients))

    def test_non_existent_recipe_not_found(self):
        Recipe.objects.all().delete()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)


class AddRecipeToFridgeTests(TestCase):
    def setUp(self):
        tmp = User.objects.create_user(username='tmp', password='test')
        self.user = User.objects.create_user(username='test', password='test')
        self.client = Client()
        self.client.login(username='test', password='test')
        self.fridge = Fridge.objects.create(user=self.user)
        self.recipe = Recipe.objects.create(author=tmp, title='test', description='')
        self.url = reverse('recipes:add_to_fridge', kwargs={'pk': self.recipe.pk})

    def test_maps_to_correct_view(self):
        r = resolve('/recipes/add_to_fridge/' + str(self.recipe.pk) + '/')

        self.assertEqual(r.view_name, 'recipes:add_to_fridge')
        self.assertEqual(r.func, add_to_fridge)

    def test_logged_in_allowed_access(self):
        redirect = reverse('fridge:fridge_detail')

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirect)

    def test_anonymous_access_not_allowed(self):
        anon = Client()
        redirect = reverse('login') + '?next=' + self.url

        response = anon.get(self.url)

        self.assertRedirects(response, redirect)

    def test_adds_recipe_to_correct_fridge(self):
        self.client.get(self.url)

        all_recipes = self.fridge.recipes.all()

        self.assertEqual(len(all_recipes), 1)
        self.assertTrue(self.recipe in all_recipes)

    def test_add_same_recipe_does_not_duplicate(self):
        self.client.get(self.url)
        self.client.get(self.url)

        all_recipes = self.fridge.recipes.all()

        self.assertEqual(len(all_recipes), 1)

    def test_diff_user_does_not_add_recipe_to_other_fridge(self):
        user = User.objects.create_user(username='test2', password='test2')
        fridge = Fridge.objects.create(user=user)
        client = Client()
        client.login(username='test2', password='test2')

        client.get(self.url)
        test2recipes = fridge.recipes.all()
        self.assertEqual(len(test2recipes), 1)

        all_recipes = self.fridge.recipes.all()
        self.assertFalse(all_recipes)

