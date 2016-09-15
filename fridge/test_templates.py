"""
Test suite for templates.
"""

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from ingredients.models import Unit, Ingredient
from recipes.models import Recipe
from .test_views import logged_in_client
from .models import Fridge, FridgeIngredient


class AddRecipeTests(TestCase):
    """ Test suite to check whether add_recipe template is correct """

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.client = logged_in_client()

    def test_add_recipe_form_is_sent(self):
        """ Ensures that a correct form is sent to a template """

        response = self.client.get(reverse('fridge:add_recipe'))
        self.assertContains(response, 'Title')
        self.assertContains(response, 'Description')
        self.assertContains(response, '')

    def test_form_invalid(self):
        """
        Ensures that missing fields are caught and an error message is shown.
        """

        potato = Ingredient.objects.create(name='Potato', type='Vegetable')
        unit = Unit.objects.create(name='kilogram', abbrev='kg')
        data = {
            'description': 'test',
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '',
            'form-0-ingredient': str(potato.pk),
            'form-0-unit': str(unit.pk),
            'form-0-quantity': '1',
        }
        response = self.client.post(reverse('fridge:add_recipe'), data)

        self.assertContains(response, 'This field is required')

        data['title'] = 'test'
        data['description'] = ''
        response = self.client.post(reverse('fridge:add_recipe'), data)

        self.assertContains(response, 'This field is required')

    def test_form_invalid_same_ingredients(self):
        """
        Ensures that the same ingredients cannot be selected and posted.
        """

        potato = Ingredient.objects.create(name='Potato', type='Vegetable')
        unit = Unit.objects.create(name='kilogram', abbrev='kg')
        data = {
            'title': 'test',
            'description': 'test',
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '',
            'form-0-ingredient': str(potato.pk),
            'form-0-unit': str(unit.pk),
            'form-0-quantity': '1',
            'form-1-ingredient': str(potato.pk),
            'form-1-unit': str(unit.pk),
            'form-1-quantity': '1',
        }

        response = self.client.post(reverse('fridge:add_recipe'), data)
        self.assertContains(response, 'Ingredients should be distinct.')

    def test_form_invalid_missing_ingredient(self):
        """
        Ensures that missing fields are caught and an error message is shown.
        """

        data = {
            'title': 'test',
            'description': 'test',
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '',
        }
        response = self.client.post(reverse('fridge:add_recipe'), data)

        self.assertContains(response, 'This field is required')


class FridgeDetailTests(TestCase):
    """ Test suite to ensure that fridge_detail template is correct """

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.client = logged_in_client()

    def test_fridge_has_add_recipe_link(self):
        """ Ensures a user sees link to add_recipe view """

        response = self.client.get(reverse('fridge:fridge_detail'))

        self.assertContains(response, '<a href="{0}">Add recipe</a>'.format(
            reverse('fridge:add_recipe')), html=True)

    def test_user_access_shows_no_ingredients(self):
        """ Ensures that nothing is shown when fridge is empty. """

        response = self.client.get(reverse('fridge:fridge_detail'))
        self.assertContains(response, 'There are no ingredients')

    def test_user_access_shows_ingredients(self):
        """ Ensures that a user is shown contents of a fridge. """

        fridge = Fridge.objects.create(user=self.user)
        unit = Unit.objects.create(name='kilogram', abbrev='kg')
        ingredient = Ingredient.objects.create(name='test', type='Fruit')
        fi = FridgeIngredient.objects.create(fridge=fridge, quantity=1,
                                             ingredient=ingredient,
                                             unit=unit)
        response = self.client.get(reverse('fridge:fridge_detail'))

        self.assertContains(response, ingredient.name)
        self.assertContains(response, ingredient.get_absolute_url())
        self.assertContains(response, fi.quantity)
        self.assertContains(response, fi.unit.abbrev)

    def test_shows_recipes(self):
        """ Ensures that a user is shown recipes in the fridge. """

        r1 = Recipe.objects.create(author=self.user, title='test',
                                   description='test')
        r2 = Recipe.objects.create(author=self.user, title='test',
                                   description='test')
        fridge = Fridge.objects.create(user=self.user)
        fridge.recipes.add(r1)

        response = self.client.get(reverse('fridge:fridge_detail'))

        self.assertContains(response, r1.title)
        self.assertContains(response, r2.title)
