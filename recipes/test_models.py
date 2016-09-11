"""
Tests suite for custom model functionality.
"""

from datetime import timezone

from django.test import TestCase
from django.contrib.auth.models import User

from .models import Recipe, Rating, RecipeIngredient
from ingredients.models import Ingredient, Unit


class RecipeTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test')
        self.r = Recipe.objects.create(author=self.user, title='test',
                                       description='')
        self.a = Recipe.objects.create(author=self.user, title='test',
                                       description='')
        self.time = timezone.now()

    def test_str_representation(self):
        """
        Test recipe string representation when there are two recipes with the
        same name.
        """
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
