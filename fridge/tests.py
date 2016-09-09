from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.admin.sites import AdminSite
from django.core.urlresolvers import reverse, resolve
from django.test.client import Client

from ingredients.models import Ingredient, Unit
from recipes.models import Recipe
from .models import Fridge, FridgeIngredient
from .admin import FridgeAdmin


class MockRequest(object):
    pass


def logged_in_client():
    """ Creates logged in user. """

    client = Client()
    client.login(username='test', password='test')
    return client


###################################
""" Test Custom Admin Functions """
###################################


class FridgeAdminTests(TestCase):
    """
    Test suite to ensure that custom functionality in Fridge admin panel
    works as expected.
    """

    def setUp(self):
        self.user = User.objects.create_user(username='test')
        self.fridge = Fridge.objects.create(user=self.user)
        self.site = AdminSite()

    def test_ingredient_list(self):
        """ Test to ensure that ingredient list shows up properly """

        i1 = Ingredient.objects.create(name='Apple', type='Fruit')
        i2 = Ingredient.objects.create(name='Orange', type='Fruit')
        FridgeIngredient.objects.create(fridge=self.fridge, ingredient=i1)
        FridgeIngredient.objects.create(fridge=self.fridge, ingredient=i2)

        expected = ", ".join([i1.name, i2.name])
        fa = FridgeAdmin(Fridge, self.site)

        self.assertEqual(fa.ingredient_list(self.fridge), expected)

    def test_recipes_list(self):
        """ Test to ensure that recipe list shows up properly """

        r1 = Recipe.objects.create(author=self.user, title='test',
                                   description='test')
        r2 = Recipe.objects.create(author=self.user, title='test2',
                                   description='test2')
        self.fridge.recipes.add(r1)
        self.fridge.recipes.add(r2)

        expected = ", ".join([r1.title, r2.title])
        fa = FridgeAdmin(Fridge, self.site)

        self.assertEqual(fa.recipe_list(self.fridge), expected)


###################################
""" Test Views, URLS & Templates"""
###################################


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


############################################
""" Tests for custom model functionality """
############################################


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
