from django.test import TestCase

from django.core.urlresolvers import reverse, resolve
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.contrib.admin.sites import AdminSite

from .models import *
from .admin import RecipeAdmin
from ingredients.models import Ingredient


###################################
""" Test Custom Admin Functions """
###################################


class RecipeAdminTests(TestCase):
    """
    Test suite to ensure that custom functionality in Fridge admin panel
    works as expected.
    """

    def setUp(self):
        self.user = User.objects.create_user(username='test')
        self.recipe = Recipe.objects.create(author=self.user, title='test')
        self.unit = Unit.objects.create(name='kilogram', abbrev='kg')
        self.site = AdminSite()

    def test_ingredient_list(self):
        """ Test to ensure that ingredient list shows up properly """

        i1 = Ingredient.objects.create(name='Apple', type='Fruit')
        i2 = Ingredient.objects.create(name='Orange', type='Fruit')
        RecipeIngredient.objects.create(recipe=self.recipe, ingredient=i1,
                                        unit=self.unit, quantity=1)
        RecipeIngredient.objects.create(recipe=self.recipe, ingredient=i2,
                                        unit=self.unit, quantity=1)

        expected = ", ".join([i1.name, i2.name])
        ma = RecipeAdmin(Recipe, self.site)

        self.assertEqual(ma.ingredient_list(self.recipe), expected)


############################################
""" Tests for custom model functionality """
############################################


class RecipeTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test')
        self.r = Recipe.objects.create(author=self.user, title='test',
                                       description='')
        self.a = Recipe.objects.create(author=self.user, title='test',
                                       description='')
        self.time = timezone.now()

    def test_str_representation(self):
        self.assertEqual(str(self.r), "{0}-{1}".format(self.r.title, self.r.pk))

    def test_date_field(self):
        """ Pretty lame test! """
        self.assertNotEquals(self.r.date, self.time)

    def test_slug_field_remains_the_same(self):
        self.r.title = 'test2'
        self.assertNotEquals(self.r.slug, slugify(self.r.title))

    def test_unique_slug_creation(self):
        self.assertEqual(self.a.slug, "{0}-{1}".format(self.a.title, 1))

    def test_slug_field_is_unique(self):
        self.assertNotEquals(self.a.slug, self.r.slug)


class RatingTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test')
        self.r = Recipe.objects.create(author=self.user, title='test',
                                       description='')
        self.rating = Rating.objects.create(user=self.user, recipe=self.r,
                                            stars=1)

    def test_str_representation(self):
        self.assertEqual(str(self.rating), "{0}\'s {1} rating: {2}".format(
            self.user.username, self.r, self.rating.stars))


class RecipeIngredientTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test')
        self.r = Recipe.objects.create(author=self.user, title='test')
        self.ingredient = Ingredient.objects.create(name='Meat', type='Meat')
        self.unit = Unit.objects.create(name='kilogram', abbrev='kg')
        self.ri = RecipeIngredient.objects.create(recipe=self.r,
                                                  ingredient=self.ingredient,
                                                  unit=self.unit, quantity=1)

    def test_str_representation(self):
        self.assertEqual(str(self.ri), "{0} in {1}".format(self.ingredient,
                                                           self.r))


###################################
""" Test Views, URLS & Templates"""
###################################


class UrlTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test')
        self.r = Recipe.objects.create(author=self.user, title='test',
                                       description='')

    def test_recipes_url(self):
        resolver = resolve('/recipes/')
        self.assertEqual(resolver.view_name, 'recipes:recipes')

    def test_recipes_detail_url(self):
        recipe_path = self.r.slug + '/'
        resolver = resolve('/recipes/' + recipe_path)
        self.assertEqual(resolver.view_name, 'recipes:recipe_detail')


class ViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test')
        self.r = Recipe.objects.create(author=self.user, title='test',
                                       description='')

    def test_recipes_view(self):
        url = reverse('recipes:recipes')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_recipe_detail_view(self):
        url = reverse('recipes:recipe_detail', kwargs={'slug': self.r.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


""" Testing helper functions """


class UserDirectoryPathTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test')
        self.r = Recipe.objects.create(author=self.user, title='test')
        self.path = user_directory_path(self.r, 'burbt')

    def test_path(self):
        self.assertEqual(self.path, "user_{0}/{1}".format(self.user.id,
                                                          'burbt'))
