from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test.client import Client

from ingredients.models import Ingredient
from .models import Fridge, FridgeIngredient


def logged_in_client():
    """ Creates logged in user. """

    client = Client()
    client.login(username='test', password='test')
    return client


class FridgeViewsURLsTestCase(TestCase):
    """
    Test suite to check whether the views associated with Fridge model are
    functioning correctly. Includes tests on views and URLs.
    """

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.fridge = Fridge.objects.create(user=self.user)
        self.client = logged_in_client()

    def test_user_access(self):
        """ Test to ensure that the user is allowed to access the fridge """

        response = self.client.get(reverse('fridge:fridge_detail'))
        self.assertEqual(response.status_code, 200)

    def test_user_access_shows_no_ingredients(self):
        """ Test to ensure that nothing is shown when fridge is empty. """

        response = self.client.get(reverse('fridge:fridge_detail'))
        self.assertContains(response, 'There are no ingredients')

    def test_user_access_shows_ingredients(self):
        """ Test to ensure that the user is shown contents of a fridge. """

        ingredient = Ingredient.objects.create(name='test', type='Fruit')
        FridgeIngredient.objects.create(fridge=self.fridge, quantity=1,
                                        ingredient=ingredient)
        response = self.client.get(reverse('fridge:fridge_detail'))

        self.assertContains(response, ingredient.name)

    # THIS SHOULD BE CHANGED IF FUNCTIONALITY EDITED TO AUTOMATICALLY ADD FRIDGE
    def test_user_access_no_fridge(self):
        """ Test to ensure that when the fridge is missing, 404 is thrown. """

        Fridge.objects.all().delete()
        response = self.client.get(reverse('fridge:fridge_detail'))

        self.assertEqual(response.status_code, 404)

    """ Needs a test with anonymous user: once logging in is implemented """


############################################
""" Tests for custom model functionality """
############################################


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
