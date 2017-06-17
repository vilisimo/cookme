from string import capwords

from django.core.urlresolvers import resolve
from django.test import TestCase
from django.utils.text import slugify

from ingredients.models import Ingredient, Unit


class IngredientTests(TestCase):
    def setUp(self):
        self.ingredient = Ingredient.objects.create(name='Meat', type='Meat')
        self.ingredient2 = Ingredient.objects.create(name='test2', type='Meat')

    def test_str_representation(self):
        expected = str(self.ingredient)

        self.assertEqual(expected, self.ingredient.name)

    def test_slug(self):
        expected_slug = slugify(self.ingredient2.name)

        self.assertEqual(expected_slug, self.ingredient2.slug)

    def test_unique_slugs(self):
        # Different name, same slugify value
        i1 = Ingredient.objects.create(name=';test:')
        i2 = Ingredient.objects.create(name=':test:')

        self.assertNotEqual(i1.slug, i2.slug)

    def test_capitalisation(self):
        name = 'test test test'

        i = Ingredient.objects.create(name=name)

        self.assertEqual(i.name, capwords(name))

    def test_absolute_url(self):
        resolver = resolve(self.ingredient2.get_absolute_url())

        self.assertEqual(resolver.view_name, 'ingredients:ingredient_detail')


class UnitTests(TestCase):
    def setUp(self):
        self.unit = Unit.objects.create(name='kilogram', abbrev='kg')

    def test_str_representation(self):
        expected_str = str(self.unit)
        unit_str = self.unit.abbrev

        self.assertEqual(expected_str, unit_str)
