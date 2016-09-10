from django.test import TestCase
from django.utils.text import slugify
from django.core.urlresolvers import resolve, reverse
from django.test.client import Client

from fridge.tests import logged_in_client
from .models import Ingredient, Unit
from .views import ingredient_detail


###################################
""" Test Views, URLS & Templates"""
###################################


class IngredientViewsURLsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.logged = logged_in_client()
        self.i = Ingredient.objects.create(name='test', type='Fruit',
                                           description='test')

    def test_URL_resolves_to_correct_view(self):
        """ Test to ensure that ingredient's URL resolves to correct view """

        view = resolve('/ingredients/' + self.i.slug + '/')

        self.assertEqual(view.func, ingredient_detail)

    def test_user_access(self):
        """ Test to ensure that all users can access ingredient details """

        response = self.client.get(reverse('ingredients:ingredient_detail',
                                   args=[self.i.slug]))
        response2 = self.logged.get(reverse('ingredients:ingredient_detail',
                                    args=[self.i.slug]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response2.status_code, 200)

    def test_no_ingredient_404(self):
        """ Test that the user is shown 404 error when there are no ingr. """

        Ingredient.objects.all().delete()

        response = self.logged.get(reverse('ingredients:ingredient_detail',
                                   args=[self.i.slug]))

        self.assertEqual(response.status_code, 404)

    def test_template_shows_correct_info(self):
        """ Test that the ingredient_detail template shows all required info """

        response = self.client.get(reverse('ingredients:ingredient_detail',
                                   args=[self.i.slug]))

        self.assertContains(response, self.i.name)
        self.assertContains(response, self.i.description)
        self.assertContains(response, self.i.type)


#######################################
""" Test custom model functionality """
#######################################


class IngredientTestCase(TestCase):
    def setUp(self):
        self.ingredient = Ingredient.objects.create(name='Meat', type='Meat')
        self.ingredient2 = Ingredient.objects.create(name='test test',
                                                     type='Meat')

    def test_str_representation(self):
        """ Test to ensure that the string representation of a model is ok """

        self.assertEqual(str(self.ingredient), self.ingredient.name)

    def test_slug(self):
        """ Test to ensure that the slug is properly created """

        self.assertEqual(slugify(self.ingredient2.name), self.ingredient2.slug)

    def test_absolute_url(self):
        """ Test to ensure that the absolute path leads to a correct view """

        resolver = resolve(self.ingredient2.get_absolute_url())

        self.assertEqual(resolver.view_name, 'ingredients:ingredient_detail')


class UnitTestCase(TestCase):
    def setUp(self):
        self.unit = Unit.objects.create(name='kilogram', abbrev='kg')

    def test_str_representation(self):
        """ Test to ensure that the string representation of a model is ok """

        unit_str = "{0} ({1})".format(self.unit.name, self.unit.abbrev)
        self.assertEqual(str(self.unit), unit_str)
