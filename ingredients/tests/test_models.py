"""
Test suite for custom model functionality.
"""

from string import capwords

from django.test import TestCase
from django.utils.text import slugify
from django.core.urlresolvers import resolve

from ingredients.models import Ingredient, Unit


class IngredientTests(TestCase):
    """ Test suite for Ingredient model. """

    def setUp(self):
        self.ingredient = Ingredient.objects.create(name='Meat', type='Meat')
        self.ingredient2 = Ingredient.objects.create(name='test test',
                                                     type='Meat')

    def test_str_representation(self):
        """
        Ensures that a string representation of an ingredient is correct.
        """

        self.assertEqual(str(self.ingredient), self.ingredient.name)

    def test_slug(self):
        """ Ensures that a slug is properly created. """

        self.assertEqual(slugify(self.ingredient2.name), self.ingredient2.slug)

    def test_unique_slugs(self):
        """
        Ensures that when names of ingredients result in the same slugify
        value, non-repeating slugs are created.
        """

        # Different name, same slugify value
        i1 = Ingredient.objects.create(name=';test:')
        i2 = Ingredient.objects.create(name=':test:')

        self.assertNotEqual(i1.slug, i2.slug)

    def test_capitalisation(self):
        """ Ensures that ingredient names are capitalized. """

        name = 'test test test'
        i = Ingredient.objects.create(name=name)

        self.assertEqual(i.name, capwords(name))

    def test_absolute_url(self):
        """ Ensures that an absolute path leads to a correct view. """

        resolver = resolve(self.ingredient2.get_absolute_url())

        self.assertEqual(resolver.view_name, 'ingredients:ingredient_detail')


class UnitsTests(TestCase):
    """ Test suite for Unit model. """

    def setUp(self):
        self.unit = Unit.objects.create(name='kilogram', abbrev='kg')

    def test_str_representation(self):
        """ Ensures that a string representation of unit is correct. """

        unit_str = self.unit.abbrev
        self.assertEqual(str(self.unit), unit_str)
