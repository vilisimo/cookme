"""
Test suite to check custom model functionality.
"""


from django.test import TestCase
from django.core.urlresolvers import resolve
from django.contrib.auth.models import User

from .models import Fridge, FridgeIngredient
from ingredients.models import Ingredient


class FridgeTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test')
        self.fridge = Fridge.objects.create(user=self.user)

    def test_str_representation(self):
        """ Test to ensure that a correct string represent. is constructed """

        self.assertEqual(str(self.fridge), "{0}'s fridge".format(
            self.user.username))

    def test_absolute_url(self):
        """ Test to ensure that the absolute URL routes to correct view """

        resolver = resolve(self.fridge.get_absolute_url())

        self.assertEqual(resolver.view_name, 'fridge:fridge_detail')


class FridgeIngredientTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test')
        self.fridge = Fridge.objects.create(user=self.user)
        self.ingredient = Ingredient.objects.create(name='Meat', type='Meat')
        self.fi = FridgeIngredient.objects.create(fridge=self.fridge,
                                                  ingredient=self.ingredient)

    def test_str_representation(self):
        """ Test to ensure that a correct string represent. is constructed """

        self.assertEquals(str(self.fi), "{0} in {1}".format(self.ingredient,
                                                            self.fridge))
