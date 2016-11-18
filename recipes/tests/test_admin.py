"""
Test suite for custom admin functions.
"""


from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User

from ingredients.models import Ingredient, Unit
from recipes.models import Recipe, RecipeIngredient
from recipes.admin import RecipeAdmin


class RecipeAdminTests(TestCase):
    """
    Test suite to ensure that custom functionality in Fridge admin panel
    works as expected. More specifically, that lists of model entities show
    up where appropriate.
    """

    def setUp(self):
        self.user = User.objects.create_user(username='test')
        self.recipe = Recipe.objects.create(author=self.user, title='test')
        self.unit = Unit.objects.create(name='kilogram', abbrev='kg')
        self.site = AdminSite()

    def test_ingredient_list(self):
        """ Ensures that ingredient list shows up properly """

        i1 = Ingredient.objects.create(name='Apple', type='Fruit')
        i2 = Ingredient.objects.create(name='Orange', type='Fruit')
        RecipeIngredient.objects.create(recipe=self.recipe, ingredient=i1,
                                        unit=self.unit, quantity=1)
        RecipeIngredient.objects.create(recipe=self.recipe, ingredient=i2,
                                        unit=self.unit, quantity=1)

        expected = ", ".join([i1.name, i2.name])
        ma = RecipeAdmin(Recipe, self.site)

        self.assertEqual(ma.ingredient_list(self.recipe), expected)

    def test_step_list(self):
        """ Ensures that steps are shown properly. """

        steps = "; ".join(['step1', 'step2'])
        recipe = Recipe.objects.create(author=self.user, title='test',
                                       steps='step1\n\nstep2')
        ma = RecipeAdmin(Recipe, self.site)

        self.assertEqual(ma.steps_display(recipe), steps)
