from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.test import TestCase

from ingredients.models import Ingredient, Unit
from recipes.admin import RecipeAdmin
from recipes.models import Recipe, RecipeIngredient


class RecipeAdminTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test')
        self.rec = Recipe.objects.create(author=self.user, title='test')
        self.unit = Unit.objects.create(name='kilogram', abbrev='kg')
        self.site = AdminSite()

    def test_ingredient_list_shown(self):
        i1 = Ingredient.objects.create(name='Apple', type='Fruit')
        i2 = Ingredient.objects.create(name='Orange', type='Fruit')
        RecipeIngredient.objects.create(recipe=self.rec, ingredient=i1, unit=self.unit, quantity=1)
        RecipeIngredient.objects.create(recipe=self.rec, ingredient=i2, unit=self.unit, quantity=1)
        expected = ", ".join([i1.name, i2.name])

        ma = RecipeAdmin(Recipe, self.site)

        self.assertEqual(ma.ingredient_list(self.rec), expected)

    def test_step_list_shown(self):
        steps = "; ".join(['step1', 'step2'])
        recipe = Recipe.objects.create(author=self.user, title='test', steps='step1\n\nstep2')

        ma = RecipeAdmin(Recipe, self.site)

        self.assertEqual(ma.steps_display(recipe), steps)
