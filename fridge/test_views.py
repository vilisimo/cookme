"""
Test suite for views, urls & templates.
"""


from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, resolve
from django.test.client import Client

from ingredients.models import Ingredient, Unit
from recipes.models import Recipe
from .models import Fridge, FridgeIngredient
from .views import fridge_detail


class MockRequest(object):
    pass


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
        self.unit = Unit.objects.create(name='kilogram', abbrev='kg',
                                        description='test')

    def test_url_resolves_to_detail_fridge(self):
        """ Test to ensure that URL resolves to a correct view function """

        view = resolve('/fridge/')

        self.assertEqual(view.func, fridge_detail)

    def test_user_access(self):
        """ Test to ensure that the user is allowed to access the fridge """

        response = self.client.get(reverse('fridge:fridge_detail'))

        self.assertEqual(response.status_code, 200)

    # Needs login page first, otherwise 404?
    # def test_anonymous_access(self):
    #     """ Test to ensure that the anonymous user is not shown a fridge """
    #
    #     cl = Client()
    #
    #     r = reverse('fridge:fridge_detail')
    #     redirect_string = 'accounts/login/?next='
    #     response = cl.get(reverse('fridge:fridge_detail'))
    #
    #     self.assertRedirects(response, redirect_string + r)

    def test_user_access_shows_no_ingredients(self):
        """ Test to ensure that nothing is shown when fridge is empty. """

        response = self.client.get(reverse('fridge:fridge_detail'))
        self.assertContains(response, 'There are no ingredients')

    def test_user_access_shows_ingredients(self):
        """ Test to ensure that the user is shown contents of a fridge. """

        ingredient = Ingredient.objects.create(name='test', type='Fruit')
        fi = FridgeIngredient.objects.create(fridge=self.fridge, quantity=1,
                                             ingredient=ingredient,
                                             unit=self.unit)
        response = self.client.get(reverse('fridge:fridge_detail'))

        self.assertContains(response, ingredient.name)
        self.assertContains(response, ingredient.get_absolute_url())
        self.assertContains(response, fi.quantity)
        self.assertContains(response, fi.unit.abbrev)

    def test_shows_recipes(self):
        """ Test to ensure that the user is shown recipes in the fridge. """

        r1 = Recipe.objects.create(author=self.user, title='test',
                                   description='test')
        r2 = Recipe.objects.create(author=self.user, title='test',
                                   description='test')
        self.fridge.recipes.add(r1)

        response = self.client.get(reverse('fridge:fridge_detail'))

        self.assertContains(response, r1.title)
        self.assertContains(response, r2.title)

    def test_user_access_no_fridge(self):
        """
        Test to ensure that when the fridge is missing, 404 is thrown. Note
        that the way it is coded right now (09-09-2016) is that upon accessing
        the home page, fridge is created. Hence, the test below
        """

        Fridge.objects.all().delete()
        response = self.client.get(reverse('fridge:fridge_detail'))

        self.assertEqual(response.status_code, 404)

    def test_user_access_no_fridge_homepage_first(self):
        """
        Test to ensure that if the user does not have the fridge and tries
        to access home page, a fridge will be created.
        """

        Fridge.objects.all().delete()

        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('fridge:fridge_detail'))
        self.assertEqual(response.status_code, 200)

    """ Needs a test with anonymous user: once logging in is implemented """


