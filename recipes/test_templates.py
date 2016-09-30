from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from ingredients.models import Ingredient, Unit
from .models import Recipe, RecipeIngredient


class RecipeTemplateTests(TestCase):
    """ Test suite to ensure that recipe list template shows what it should. """

    def setUp(self):
        self.client = Client()
        self.url = reverse('recipes:recipes')
        self.u = User.objects.create_user(username='test', password='test')
        self.r1 = Recipe.objects.create(author=self.u, title='test1',
                                        description='test1')
        self.r2 = Recipe.objects.create(author=self.u, title='test2',
                                        description='test2')

    def test_recipes_template_recipes(self):
        """ Ensures that the template shows all recipes. """

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.r1.title)
        self.assertContains(response, self.r2.title)

    def test_recipes_template_author(self):
        """ Ensures that the author is shown. """

        response = self.client.get(self.url)

        self.assertContains(response, self.r1.author)
        self.assertContains(response, self.r2.author)

    def test_has_add_recipe_to_fridge(self):
        """
        Ensures that the template has a link to add a recipe to a fridge.

        Note that there is small hardcoded part (Add), which may be removed
        when the project moves to jQuery.
        """

        add_to_fridge = reverse('recipes:add_to_fridge',
                                kwargs={'pk': self.r1.pk})
        ahref = '<a href="{}">Add</a>'.format(add_to_fridge)
        response = self.client.get(self.url)

        self.assertContains(response, ahref, html=True)


class RecipeDetailTemplateTests(TestCase):
    """ Test suite to ensure that recipe detail template is correct. """

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test', password='test')
        self.r1 = Recipe.objects.create(author=self.user, title='test1',
                                        description='test1')

        self.i1 = Ingredient.objects.create(name='apple', type='Fruit')
        self.i2 = Ingredient.objects.create(name='orange', type='Orange')
        self.unit = Unit.objects.create(name='kilogram', abbrev='kg')

        RecipeIngredient.objects.create(recipe=self.r1, ingredient=self.i1,
                                        unit=self.unit, quantity=0.5)
        RecipeIngredient.objects.create(recipe=self.r1, ingredient=self.i2,
                                        unit=self.unit, quantity=0.5)
        self.url = reverse('recipes:recipe_detail', kwargs={'slug':
                                                            self.r1.slug})

    def test_recipe_detail_ingredients(self):
        """ Ensures that all ingredients are listed. """

        response = self.client.get(self.url)

        self.assertContains(response, self.i1)
        self.assertContains(response, self.i2)

    def test_recipe_detail_ingredient_quantity(self):
        """ Ensures that quantity is shown. """

        ingredient = RecipeIngredient.objects.all()

        response = self.client.get(self.url)

        self.assertContains(response, ingredient[0].quantity)
        self.assertContains(response, ingredient[1].quantity)

    def test_recipe_detail_unit(self):
        """ Ensures that units are shown. """

        response = self.client.get(self.url)

        self.assertContains(response, self.unit.abbrev)

    def test_recipe_detail_one_step(self):
        """ Ensures that default value is shown correctly in the template. """

        response = self.client.get(self.url)

        self.assertEqual(response.context['steps'], self.r1.step_list())
        self.assertContains(response, "<p>{0}</p>".format(self.r1.steps),
                            html=True)

    def test_recipe_detail_one_step_non_default(self):
        """ Ensures that non-default value is shown in the template. """

        recipe = Recipe.objects.create(author=self.user, title='test',
                                       description='test', steps='step1')
        url = reverse('recipes:recipe_detail', kwargs={'slug': recipe.slug})
        response = self.client.get(url)

        self.assertEqual(response.context['steps'], recipe.step_list())
        self.assertContains(response, "<p>{0}</p>".format(recipe.steps),
                            html=True)

    def test_recipe_detail_two_steps(self):
        """
        Ensures that when two or more steps are given, they are correctly
        labeled as "step [n]".
        """

        recipe = Recipe.objects.create(author=self.user, title='test',
                                       description='test',
                                       steps='step1\n\nstep2')
        steps = recipe.step_list()
        url = reverse('recipes:recipe_detail', kwargs={'slug': recipe.slug})
        response = self.client.get(url)

        self.assertEqual(response.context['steps'], steps)
        self.assertContains(response, "<p>{0}</p>".format(steps[1]), html=True)

    def test_recipe_cuisine(self):
        """
        Ensures recipe_detail template shows cuisine the recipe comes form.
        """

        r = Recipe.objects.create(author=self.user, title='test',
                                  description='test')
        url = reverse('recipes:recipe_detail', kwargs={'slug': r.slug})
        response = self.client.get(url)

        self.assertEqual(response.context['cuisine'], r.get_cuisine_display())
        self.assertContains(response, r.get_cuisine_display())

        r = Recipe.objects.create(author=self.user, title='test',
                                  description='test', cuisine='fr')
        url = reverse('recipes:recipe_detail', kwargs={'slug': r.slug})
        response = self.client.get(url)

        self.assertContains(response, r.get_cuisine_display())



