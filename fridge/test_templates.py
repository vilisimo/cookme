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
    """ Test suite to check whether add_recipe template is correct. """

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.client = logged_in_client()

    def test_add_recipe_form_is_sent(self):
        """ Ensures that a form & formset is sent to a template. """

        response = self.client.get(reverse('fridge:add_recipe'))
        self.assertIn('form', response.context)
        self.assertIn('formset', response.context)

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

        self.assertContains(response, 'This field is required.')

        data['title'] = 'test'
        data['description'] = '   '
        response = self.client.post(reverse('fridge:add_recipe'), data)

        self.assertContains(response, 'This field is required.')

        data['description'] = 'test'
        data['cuisine'] = ''
        response = self.client.post(reverse('fridge:add_recipe'), data)

        self.assertContains(response, 'This field is required.')

        data['cuisine'] = 'ot'
        data['steps'] = '   '
        response = self.client.post(reverse('fridge:add_recipe'), data)

        self.assertContains(response, 'This field is required.')

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
        Ensures that ingredients are required and skipping them is not allowed.
        Error message should be shown, in case HTML validation fails.
        """

        data = {
            'title': 'test',
            'description': 'test',
            'cuisine': 'ot',
            'steps': 'step1',
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '',
        }
        response = self.client.post(reverse('fridge:add_recipe'), data)

        self.assertContains(response, 'This field is required.')


class FridgeDetailFridgeIngredientFormTests(TestCase):
    """ Test suite to ensure that FridgeIngredient form performs well. """

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.unit = Unit.objects.create(name='kilogram', abbrev='kg')
        self.client = logged_in_client()

    def test_form_no_ingredient(self):
        """ Ensure that when no ingredient is given, error is shown. """

        url = reverse('fridge:fridge_detail')
        data = {'ingredient': '', 'unit': self.unit, 'quantity': 1}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required.')

    def test_form_no_unit(self):
        """ Ensure that when no unit is given, error is shown. """

        url = reverse('fridge:fridge_detail')
        data = {'ingredient': 'test', 'unit': '', 'quantity': 1}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required.')

    def test_form_no_quantity(self):
        """ Ensure that when no quantity is given, error is shown. """

        url = reverse('fridge:fridge_detail')
        data = {'ingredient': 'test', 'unit': self.unit.pk}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)
        # why is 'ingredient': None allowed? Different error than required?
        self.assertContains(response, 'This field is required.')

    def test_form_is_shown(self):
        """
        Ensures that a form is shown to a user. Dubious value: string may
        change.
        """

        url = reverse('fridge:fridge_detail')
        response = self.client.get(url)

        self.assertContains(response, 'Add Ingredient')


class FridgeDetailTests(TestCase):
    """ Test suite to ensure that fridge_detail template is correct. """

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.client = logged_in_client()

    def test_fridge_has_add_recipe_link(self):
        """ Ensures a user sees link to add_recipe view. """

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

    def test_shows_remove(self):
        """ Ensures that a template has shows a remove function. """

        i1 = Ingredient.objects.create(name='test1', type='Fruit')
        unit = Unit.objects.create(name='kilogram', abbrev='kg')
        fridge = Fridge.objects.create(user=self.user)
        fi1 = FridgeIngredient.objects.create(fridge=fridge,
                                              ingredient=i1,
                                              unit=unit,
                                              quantity=1)

        url = reverse('fridge:fridge_detail')
        response = self.client.get(url)

        self.assertContains(response, '<a href="{0}">Remove</a>'.format(reverse(
            'fridge:remove_ingredient', kwargs={'pk': fi1.pk})), html=True)
