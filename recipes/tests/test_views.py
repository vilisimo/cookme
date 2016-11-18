"""
Test suite for views, urls & templates.
"""


from django.test import TestCase

from django.core.urlresolvers import resolve
from django.test.client import Client

from fridge.models import Fridge
from recipes.models import *
from recipes.views import recipes, recipe_detail, add_to_fridge


class URLTests(TestCase):
    """ Test suite to ensure that the view is mapped to a correct url. """

    def setUp(self):
        self.user = User.objects.create_user(username='test')
        self.r = Recipe.objects.create(author=self.user, title='test',
                                       description='')

    def test_recipes_url(self):
        """ Ensures that a user is shown a correct URL for recipes. """

        resolver = resolve('/recipes/')

        self.assertEqual(resolver.view_name, 'recipes:recipes')
        self.assertEqual(resolver.func, recipes)

    def test_recipes_detail_url(self):
        """
        Ensures that a user is shown a correct URL for recipe detail page.
        """

        recipe_path = self.r.slug + '/'
        resolver = resolve('/recipes/' + recipe_path)

        self.assertEqual(resolver.view_name, 'recipes:recipe_detail')
        self.assertEqual(resolver.func, recipe_detail)


class RecipeViewTests(TestCase):
    """ Test suite to ensure that Recipes view works correctly. """

    def setUp(self):
        self.client = Client()
        self.url = reverse('recipes:recipes')

    def test_recipes_view(self):
        """
        Ensures that the recipes view renders correctly.

        Note: the view does not require a user to be logged in. Hence,
        there is no need to test both situations (logged in vs. anonymous)
        """

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)


class RecipeDetailTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test')
        self.r = Recipe.objects.create(author=self.user, title='test',
                                       description='')
        self.url = reverse('recipes:recipe_detail',
                           kwargs={'slug': self.r.slug})

    def test_recipe_detail_view(self):
        """ Ensures that recipe detail view renders correctly. """

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_recipe_detail_view_context(self):
        """ Test to ensure that the context is passed correct arguments. """

        ingredient = Ingredient.objects.create(name='apple', type='Fruit')
        unit = Unit.objects.create(name='kilogram', abbrev='kg')
        RecipeIngredient.objects.create(recipe=self.r, ingredient=ingredient,
                                        unit=unit, quantity=0.5)
        ingredients = RecipeIngredient.objects.filter(recipe=self.r)
        response = self.client.get(self.url)

        # QuerySets are not equal even if they contain the same values,
        # hence we need to convert them to lists.
        self.assertEqual(list(response.context['ingredients']),
                         list(ingredients))

    def test_non_existent_recipe(self):
        """ Ensures that non-existent recipe throws 404. """

        Recipe.objects.all().delete()
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 404)


class AddRecipeToFridgeTests(TestCase):
    """
    Test suite to ensure that a user can add a recipe to his/her fridge
    without any major issues.
    """

    def setUp(self):
        tmp = User.objects.create_user(username='tmp', password='test')
        self.user = User.objects.create_user(username='test', password='test')
        self.client = Client()
        self.client.login(username='test', password='test')
        self.fridge = Fridge.objects.create(user=self.user)
        self.recipe = Recipe.objects.create(author=tmp, title='test',
                                            description='')
        self.url = reverse('recipes:add_to_fridge',
                           kwargs={'pk': self.recipe.pk})

    def test_correct_view(self):
        """ Ensures URL routes to correct view. """

        r = resolve('/recipes/add_to_fridge/' + str(self.recipe.pk) + '/')

        self.assertEqual(r.view_name, 'recipes:add_to_fridge')
        self.assertEqual(r.func, add_to_fridge)

    def test_access(self):
        """ Ensures that logged in user can access the view. """

        response = self.client.get(self.url)
        redirect = reverse('fridge:fridge_detail')

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect)

    def test_anonymous_access(self):
        """ Ensures non-logged in user cannot access the view. """

        anon = Client()
        response = anon.get(self.url)
        redirect = reverse('login') + '?next=' + self.url

        self.assertRedirects(response, redirect)

    def test_adds_recipe(self):
        """ Ensures that the view adds recipe to a correct fridge. """

        self.client.get(self.url)
        recipes = self.fridge.recipes.all()

        self.assertEqual(len(recipes), 1)
        self.assertTrue(self.recipe in recipes)

    def test_add_same_recipe(self):
        """
        Ensure that adding the same recipe does not duplicate it in user's
        fridge.
        """

        self.client.get(self.url)
        self.client.get(self.url)
        recipes = self.fridge.recipes.all()

        self.assertEqual(len(recipes), 1)

    def test_diff_user(self):
        """
        Ensures that if a different user adds recipe to his/her fridge,
        this is not reflected in other users' fridges.
        """

        u = User.objects.create_user(username='test2', password='test2')
        f = Fridge.objects.create(user=u)
        c = Client()
        c.login(username='test2', password='test2')

        c.get(self.url)
        test2recipes = f.recipes.all()

        self.assertEqual(len(test2recipes), 1)

        recipes = self.fridge.recipes.all()

        self.assertFalse(recipes)

