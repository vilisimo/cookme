from string import capwords

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from django.utils.text import slugify

from ingredients.models import Ingredient, Unit
from recipes.models import Recipe, Rating, RecipeIngredient, user_directory_path


class RecipeTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test')
        self.r = Recipe.objects.create(author=self.user, title='test', description='')
        self.a = Recipe.objects.create(author=self.user, title='test', description='')
        self.time = timezone.now()

    def test_description_default_upon_missing_description(self):
        test_recipe = Recipe.objects.create(author=self.user, title='test')

        self.assertTrue(test_recipe.description)
        self.assertEquals(test_recipe.description, "No description provided.")

    def test_steps_default_upon_missing_steps(self):
        test_recipe = Recipe.objects.create(author=self.user, title='test')

        self.assertTrue(test_recipe.steps)
        self.assertEquals(test_recipe.steps, "No steps provided. Time to get creative!")

    def test_steps_split_when_newlines_entered(self):
        expected = ['step1', 'step2']

        recipe = Recipe.objects.create(author=self.user, title='test', steps='step1\n\nstep2')

        self.assertEqual(recipe.step_list(), expected)

    def test_str_representation(self):
        recipe = Recipe.objects.create(author=self.user, title='another', description='')

        self.assertEqual(str(recipe), recipe.title)

    def test_str_representation_two_same_recipe_names_are_same(self):
        self.assertEqual(str(self.r), self.r.title)

    def test_date_field(self):
        """ Pretty lame test! """

        self.assertNotEquals(self.r.date, self.time)

    def test_slug_field_remains_the_same_upon_title_change(self):
        title = self.r.title

        self.r.title = 'test2'

        self.assertEqual(self.r.slug, title.lower())
        self.assertNotEquals(self.r.slug, slugify(self.r.title))

    def test_unique_slug_creation(self):
        count = len(Recipe.objects.all())
        # Need to turn chars into lower form, as title is capitalized.
        expected = f'{self.a.title.lower()}-{count}'

        self.assertEqual(self.a.slug, expected)

    def test_capitalisation(self):
        title = 'test test test'

        r = Recipe.objects.create(author=self.user, title=title)

        self.assertEqual(r.title, capwords(title))

    def test_slug_field_is_unique(self):
        self.assertNotEquals(self.a.slug, self.r.slug)


class RatingTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test')
        self.r = Recipe.objects.create(author=self.user, title='test', description='')
        self.rating = Rating.objects.create(user=self.user, recipe=self.r, stars=1)

    def test_str_representation(self):
        username = self.user.username
        stars = self.rating.stars
        expected = f'{username}\'s {self.r} rating: {stars}'

        self.assertEqual(str(self.rating), expected)


class RecipeIngredientTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test')
        self.r = Recipe.objects.create(author=self.user, title='test')
        self.i = Ingredient.objects.create(name='Meat', type='Meat')
        self.unit = Unit.objects.create(name='kilogram', abbrev='kg')
        self.ri = RecipeIngredient.objects.create(recipe=self.r, ingredient=self.i, unit=self.unit,
                                                  quantity=1)

    def test_str_representation(self):
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
