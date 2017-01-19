"""
Tests suite for custom model functionality.
"""

from string import capwords

from django.utils import timezone
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils.text import slugify

from recipes.models import Recipe, Rating, RecipeIngredient, user_directory_path
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
        default = "No description provided."

        self.assertTrue(test_recipe.description)
        self.assertEquals(test_recipe.description, default)

    def test_steps_default(self):
        """
        Ensures that when steps are not provided, a default value is given.
        """

        test_recipe = Recipe.objects.create(author=self.user, title='test')
        default = "No steps provided. Time to get creative!"

        self.assertTrue(test_recipe.steps)
        self.assertEquals(test_recipe.steps, default)

    def test_steps_newlines(self):
        """
        Ensures that a steps are split when one or more newlines are
        encountered.
        """

        expected = ['step1', 'step2']
        recipe = Recipe.objects.create(author=self.user, title='test',
                                       steps='step1\n\nstep2')

        self.assertEqual(recipe.step_list(), expected)

    def test_str_representation_one_name(self):
        """ Ensures that string representation is correct. """

        recipe = Recipe.objects.create(author=self.user, title='another',
                                       description='')

        self.assertEqual(str(recipe), recipe.title)

    def test_str_representation_two_same_names(self):
        """
        Test recipe string representation when there are two recipes with the
        same name. Should be the same.
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
        # Need to turn chars into lower form, as title is capitalized.
        expected = f'{self.a.title.lower()}-{count}'

        self.assertEqual(self.a.slug, expected)

    def test_capitalisation(self):
        """ Ensures that ingredient names are capitalized. """

        title = 'test test test'
        r = Recipe.objects.create(author=self.user, title=title)

        self.assertEqual(r.title, capwords(title))

    def test_slug_field_is_unique(self):
        """
        Ensures that a unique slug is created for every recipe, even when
        they share the same titles.
        """

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

        username = self.user.username
        stars = self.rating.stars
        expected = f'{username}\'s {self.r} rating: {stars}'

        self.assertEqual(str(self.rating), expected)


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

        expected = f'{self.i} in {self.r}'

        self.assertEqual(str(self.ri), expected)


# Function is currently not used.
class UserDirectoryPathTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test')
        self.r = Recipe.objects.create(author=self.user, title='test')
        self.path = user_directory_path(self.r, 'test-path')

    def test_path(self):
        """ Ensure that a constructed path is correct. """

        expected = f'user_{self.user.id}/test-path'

        self.assertEqual(self.path, expected)
