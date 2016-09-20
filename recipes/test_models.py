"""
Tests suite for custom model functionality.
"""

from django.utils import timezone
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils.text import slugify

from .models import Recipe, Rating, RecipeIngredient, user_directory_path
from ingredients.models import Ingredient, Unit


class RecipeTestCase(TestCase):
    """ Test suite for Recipe model. """

    def setUp(self):
        self.user = User.objects.create(username='test')
        self.r = Recipe.objects.create(author=self.user, title='test',
                                       description='')
        self.a = Recipe.objects.create(author=self.user, title='test',
                                       description='')
        self.time = timezone.now()

    def test_description_default(self):
        """
        Ensures that when description is not provided, a default value is given.
        """

        test_recipe = Recipe.objects.create(author=self.user, title='test')
        self.assertTrue(test_recipe.description)
        self.assertTrue(test_recipe.description == "No description provided.")

    def test_steps_default(self):
        """
        Ensures that when steps are not provided, a default value is given.
        """

        test_recipe = Recipe.objects.create(author=self.user, title='test')

        self.assertTrue(test_recipe.steps)
        self.assertTrue(test_recipe.steps ==
                        "No steps provided. Time to get creative!")

    def test_steps_newlines(self):
        """
        Ensures that a steps are split when one or more newlines are
        encountered.
        """

        steps_split = ['step1', 'step2']
        recipe = Recipe.objects.create(author=self.user, title='test',
                                       steps='step1\n\nstep2')

        self.assertEqual(recipe.step_list(), steps_split)

    def test_str_representation_one_name(self):
        """ Ensures that string representation is correct. """

        recipe = Recipe.objects.create(author=self.user, title='another',
                                       description='')

        self.assertEqual(str(recipe), recipe.title)

    def test_str_representation_two_same_names(self):
        """
        Test recipe string representation when there are two recipes with the
        same name. Should be the same (as str repr. is established at run-time,
        it makes little sense to make them different - it's just confusing).
        """

        self.assertEqual(str(self.r), self.r.title)

    def test_date_field(self):
        """ Pretty lame test! """

        self.assertNotEquals(self.r.date, self.time)

    def test_slug_field_remains_the_same(self):
        """
        Ensures that even when the title changes, the slug remains the same
        to avoid broken links.
        """

        self.r.title = 'test2'
        self.assertNotEquals(self.r.slug, slugify(self.r.title))

    def test_unique_slug_creation(self):
        """ Ensures that a unique slug is created for every recipe. """

        count = len(Recipe.objects.all())

        self.assertEqual(self.a.slug, "{0}-{1}".format(self.a.title, count))

    def test_slug_field_is_unique(self):
        """ Ensures that a unique slug is created for every recipe. """

        self.assertNotEquals(self.a.slug, self.r.slug)


class RatingTestCase(TestCase):
    """ Test suite for Rating model. """

    def setUp(self):
        self.user = User.objects.create(username='test')
        self.r = Recipe.objects.create(author=self.user, title='test',
                                       description='')
        self.rating = Rating.objects.create(user=self.user, recipe=self.r,
                                            stars=1)

    def test_str_representation(self):
        """ Ensures that rating's string representation is correct. """

        self.assertEqual(str(self.rating), "{0}\'s {1} rating: {2}".format(
            self.user.username, self.r, self.rating.stars))


class RecipeIngredientTestCase(TestCase):
    """ Test suite for RecipeIngredient model. """

    def setUp(self):
        self.user = User.objects.create(username='test')
        self.r = Recipe.objects.create(author=self.user, title='test')
        self.i = Ingredient.objects.create(name='Meat', type='Meat')
        self.unit = Unit.objects.create(name='kilogram', abbrev='kg')
        self.ri = RecipeIngredient.objects.create(recipe=self.r,
                                                  ingredient=self.i,
                                                  unit=self.unit, quantity=1)

    def test_str_representation(self):
        """ Ensures that RecipeIngredient string representation is correct. """

        self.assertEqual(str(self.ri), "{0} in {1}".format(self.i, self.r))


""" Testing helper functions """


# Function is currently not used.
class UserDirectoryPathTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test')
        self.r = Recipe.objects.create(author=self.user, title='test')
        self.path = user_directory_path(self.r, 'burbt')

    def test_path(self):
        """ Ensure that a constructed path is correct. """
        self.assertEqual(self.path, "user_{0}/{1}".format(self.user.id,
                                                          'burbt'))
