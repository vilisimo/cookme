from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from ingredients.models import Ingredient, Unit
from .models import Recipe, RecipeIngredient


class RecipeTemplateTests(TestCase):
    """ Test suite to ensure that recipe template shows what it should """

    def setUp(self):
        self.client = Client()
        self.u = User.objects.create_user(username='test', password='test')
        self.r1 = Recipe.objects.create(author=self.u, title='test1',
                                        description='test1')
        self.r2 = Recipe.objects.create(author=self.u, title='test2',
                                        description='test2')

    def test_recipes_template_recipes(self):
        """ Ensures that the template shows all recipes """

        url = reverse('recipes:recipes')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.r1.title)
        self.assertContains(response, self.r2.title)

    def test_recipes_template_author(self):
        """ Ensures that the author is shown """

        url = reverse('recipes:recipes')
        response = self.client.get(url)

        self.assertContains(response, self.r1.author)
        self.assertContains(response, self.r2.author)


class RecipeDetailTemplateTests(TestCase):
    """ Test suite to ensure that recipe detail template is correct"""

    def setUp(self):
        self.client = Client()
        self.u = User.objects.create_user(username='test', password='test')
        self.r1 = Recipe.objects.create(author=self.u, title='test1',
                                        description='test1')

        self.i = Ingredient.objects.create(name='apple', type='Fruit')
        self.i2 = Ingredient.objects.create(name='orange', type='Orange')
        self.u = Unit.objects.create(name='kilogram', abbrev='kg')

        RecipeIngredient.objects.create(recipe=self.r1, ingredient=self.i,
                                        unit=self.u, quantity=0.5)
        RecipeIngredient.objects.create(recipe=self.r1, ingredient=self.i2,
                                        unit=self.u, quantity=0.5)

    def test_recipe_detail_ingredients(self):
        """ Ensures that all ingredients are listed """

        url = reverse('recipes:recipe_detail', kwargs={'slug': self.r1.slug})
        response = self.client.get(url)

        self.assertContains(response, self.i)
        self.assertContains(response, self.i2)

    def test_recipe_detail_ingredient_quantity(self):
        """ Ensures that quantity is shown """

        ingredient = RecipeIngredient.objects.all()

        url = reverse('recipes:recipe_detail', kwargs={'slug': self.r1.slug})
        response = self.client.get(url)

        self.assertContains(response, ingredient[0].quantity)
        self.assertContains(response, ingredient[1].quantity)

    def test_recipe_detail_unit(self):
        """ Ensures that units are shown """

        url = reverse('recipes:recipe_detail', kwargs={'slug': self.r1.slug})
        response = self.client.get(url)

        self.assertContains(response, self.u.abbrev)
