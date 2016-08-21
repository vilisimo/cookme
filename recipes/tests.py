from django.test import TestCase

from .models import *
from ingredients.models import Ingredient

from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse, resolve
from django.contrib.auth.models import User


""" Testing models """


class IngredientTestCase(TestCase):
    def setUp(self):
        Ingredient.objects.create(name='Meat', type='Meat')

    def test_str_representation(self):
        ingredient = Ingredient.objects.get(name='Meat')
        self.assertEqual(str(ingredient), ingredient.name)


class RecipeTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test')
        self.r = Recipe.objects.create(author=self.user, title='test',
                                       description='')
        self.a = Recipe.objects.create(author=self.user, title='test',
                                       description='')
        self.time = timezone.now()

    def test_str_representation(self):
        self.assertEqual(str(self.r), self.r.title)

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


class FridgeTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test')
        self.fridge = Fridge.objects.create(user=self.user)

    def test_str_representation(self):
        self.assertEqual(str(self.fridge), "{0}'s fridge".format(
            self.user.username))


class FridgeIngredientTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test')
        self.fridge = Fridge.objects.create(user=self.user)
        self.ingredient = Ingredient.objects.create(name='Meat', type='Meat')
        self.fi = FridgeIngredient.objects.create(fridge=self.fridge,
                                                  ingredient=self.ingredient)

    def test_str_representation(self):
        self.assertEquals(str(self.fi), "{0} in {1}".format(self.ingredient,
                                                            self.fridge))


class RecipeIngredientTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test')
        self.r = Recipe.objects.create(author=self.user, title='test')
        self.ingredient = Ingredient.objects.create(name='Meat', type='Meat')
        self.unit = Unit.objects.create(unit='Kilogram', abbrev='kg')
        self.ri = RecipeIngredient.objects.create(recipe=self.r,
                                                  ingredient=self.ingredient,
                                                  unit=self.unit, quantity=1)

    def test_str_representation(self):
        self.assertEqual(str(self.ri), "{0} in {1}".format(self.ingredient,
                                                           self.r))


""" Testing URLs & views """


class UrlTestCase(TestCase):
    def test_recipes_url(self):
        resolver = resolve('/recipes/')
        self.assertEqual(resolver.view_name, 'recipes')


class ViewsTestCase(TestCase):
    def test_recipes_view(self):
        response = self.client.get(reverse('recipes'))
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
