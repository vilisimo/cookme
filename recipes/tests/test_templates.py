from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from ingredients.models import Ingredient, Unit
from recipes.models import Recipe, RecipeIngredient


class RecipeTemplateTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('recipes:recipes')
        self.u = User.objects.create_user(username='test', password='test')
        self.r1 = Recipe.objects.create(author=self.u, title='test1', description='test1')
        self.r2 = Recipe.objects.create(author=self.u, title='test2', description='test2')

    def test_correct_template_used(self):
        response = self.client.get(self.url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipes.html')

    def test_template_shows_recipes(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.r1.title)
        self.assertContains(response, self.r2.title)

    def test_template_shows_author(self):
        response = self.client.get(self.url)

        self.assertContains(response, self.r1.author)
        self.assertContains(response, self.r2.author)

    def test_has_add_recipe_to_fridge(self):
        """
        Note that there is small hardcoded part (Add), which may be removed
        when the project moves on to writing custom jQuery scripts.
        """

        add_link = reverse('recipes:add_to_fridge', kwargs={'pk': self.r1.pk})
        expected_html = f'<a href="{add_link}" class="add-fridge">'
        self.client.login(username='test', password='test')

        response = self.client.get(self.url)

        self.assertContains(response, expected_html)

    def test_add_link_not_shown_to_anonymous(self):
        add_url = reverse('recipes:add_to_fridge', kwargs={'pk': self.r1.pk})
        expected_html = f'<a href={add_url}>Add</a>'

        response = self.client.get(self.url)

        self.assertNotContains(response, expected_html, html=True)


class RecipeDetailTemplateTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test', password='test')
        self.r1 = Recipe.objects.create(author=self.user, title='test1', description='test1')

        self.i1 = Ingredient.objects.create(name='apple', type='Fruit')
        self.i2 = Ingredient.objects.create(name='orange', type='Orange')
        self.unit = Unit.objects.create(name='kilogram', abbrev='kg')

        RecipeIngredient.objects.create(recipe=self.r1, ingredient=self.i1, unit=self.unit,
                                        quantity=0.5)
        RecipeIngredient.objects.create(recipe=self.r1, ingredient=self.i2, unit=self.unit,
                                        quantity=0.5)
        self.url = reverse('recipes:recipe_detail', kwargs={'slug': self.r1.slug})

    def test_correct_template_used(self):
        response = self.client.get(self.url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipe_detail.html')

    def test_recipe_detail_ingredients_are_shown(self):
        response = self.client.get(self.url)

        self.assertContains(response, self.i1)
        self.assertContains(response, self.i2)

    def test_ingredient_quantity_is_shown(self):
        ingredient = RecipeIngredient.objects.all()

        response = self.client.get(self.url)

        self.assertContains(response, ingredient[0].quantity)
        self.assertContains(response, ingredient[1].quantity)

    def test_units_are_shown(self):
        response = self.client.get(self.url)

        self.assertContains(response, self.unit.abbrev)

    def test_step_default_value_shown(self):
        """ Ensures that default value is shown correctly in the template. """

        expected_html = f'<p class="recipe-step">{self.r1.steps}</p>'

        response = self.client.get(self.url)

        self.assertEqual(response.context['steps'], self.r1.step_list())
        self.assertContains(response, expected_html, html=True)

    def test_recipe_detail_one_step_non_default_shown(self):
        recipe = Recipe.objects.create(author=self.user, title='test', description='test',
                                       steps='step1')
        url = reverse('recipes:recipe_detail', kwargs={'slug': recipe.slug})
        expected_html = f'<p class="recipe-step">{recipe.steps}</p>'

        response = self.client.get(url)

        self.assertEqual(response.context['steps'], recipe.step_list())
        self.assertContains(response, expected_html, html=True)

    def test_recipe_detail_two_steps_are_correctly_labeled(self):
        """
        Ensures that when two or more steps are given, they are correctly
        labeled as "step [n]".
        """

        self.r1.steps = 'step1\n\nstep2'
        self.r1.save()
        steps = self.r1.step_list()
        url = reverse('recipes:recipe_detail', kwargs={'slug': self.r1.slug})
        expected_html = f'<p class="recipe-step">{steps[1]}</p>'

        response = self.client.get(url)

        self.assertEqual(response.context['steps'], steps)
        self.assertContains(response, expected_html, html=True)

    def test_other_is_assigned_to_recipe_cuisine(self):
        url = reverse('recipes:recipe_detail', kwargs={'slug': self.r1.slug})
        cuisine_readable = self.r1.get_cuisine_display()

        response = self.client.get(url)

        self.assertEqual(response.context['cuisine'], cuisine_readable)
        self.assertContains(response, cuisine_readable)

    def test_readable_form_assigned_to_recipe_cuisine(self):
        self.r1.cuisine = 'fr'
        self.r1.save()
        url = reverse('recipes:recipe_detail', kwargs={'slug': self.r1.slug})
        cuisine_readable = self.r1.get_cuisine_display()

        response = self.client.get(url)

        self.assertContains(response, cuisine_readable)



