"""
Test suite for templates to ensure that they contain information that must be
shown never mind the style used.
"""

from http import HTTPStatus

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from fridge.models import Fridge, FridgeIngredient as FI
from ingredients.models import Unit, Ingredient
from recipes.models import Recipe
from utilities.mock_db import (
    logged_in_client, populate_recipes, populate_fridge_ingredients,
)


class AddRecipeTests(TestCase):
    """ Test suite to check whether add_recipe template is correct. """

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.potato = Ingredient.objects.create(name='Potato', type='Vegetable')
        self.unit = Unit.objects.create(name='kilogram', abbrev='kg')
        self.client = logged_in_client()
        self.data = {
            'description': 'test',
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '',
            'form-0-ingredient': str(self.potato.pk),
            'form-0-unit': str(self.unit.pk),
            'form-0-quantity': '1',
        }

    def test_add_recipe_form_is_sent(self):
        """ Ensures that a form & formset is sent to a template. """

        url = reverse('fridge:add_recipe')
        response = self.client.get(url)

        self.assertIn('form', response.context)
        self.assertIn('formset', response.context)

    def test_form_invalid(self):
        """
        Ensures that when all information is missing, an error message is shown.
        """

        response = self.client.post(reverse('fridge:add_recipe'), self.data)

        self.assertContains(response, 'This field is required.')

    def test_form_invalid_missing_description(self):
        """
        Ensures that when description field is missing, form is considered to
        be invalid.
        """

        self.data['title'] = 'test'
        self.data['description'] = '   '
        self.data['cuisine'] = 'ot'
        self.data['steps'] = 'step'
        response = self.client.post(reverse('fridge:add_recipe'), self.data)

        self.assertContains(response, 'This field is required.')

    def test_form_invalid_missing_cuisine(self):
        """
        Ensures that when cuisine field is missing, form is considered to be
        invalid.
        """

        self.data['title'] = 'test'
        self.data['description'] = 'test'
        self.data['cuisine'] = '  '
        self.data['steps'] = 'step'
        response = self.client.post(reverse('fridge:add_recipe'), self.data)

        self.assertContains(response, 'This field is required.')

    def test_form_invalid_missing_steps(self):
        """
        Ensures that when steps field is missing, form is considered to be
        invalid.
        """

        self.data['title'] = 'test'
        self.data['description'] = 'test'
        self.data['cuisine'] = 'ot'
        self.data['steps'] = '   '
        response = self.client.post(reverse('fridge:add_recipe'), self.data)

        self.assertContains(response, 'This field is required.')

    def test_form_invalid_same_ingredients(self):
        """
        Ensures that the same ingredients cannot be selected and posted.
        """

        self.data['form-0-ingredient'] = str(self.potato.pk)
        self.data['form-1-ingredient'] = str(self.potato.pk)
        self.data['form-1-unit'] = str(self.unit.pk)
        self.data['form-1-quantity'] = '1'
        response = self.client.post(reverse('fridge:add_recipe'), self.data)

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
    """ Test suite to ensure that FridgeIngredientForm performs well. """

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.unit = Unit.objects.create(name='kilogram', abbrev='kg')
        self.client = logged_in_client()

    def test_form_no_ingredient(self):
        """ Ensure that when no ingredient is given, error is shown. """

        url = reverse('fridge:fridge_detail')
        data = {'ingredient': '', 'unit': self.unit, 'quantity': 1}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'This field is required.')

    def test_form_no_unit(self):
        """ Ensure that when no unit is given, error is shown. """

        url = reverse('fridge:fridge_detail')
        data = {'ingredient': 'test', 'unit': '', 'quantity': 1}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'This field is required.')

    def test_form_no_quantity(self):
        """ Ensure that when no quantity is given, error is shown. """

        url = reverse('fridge:fridge_detail')
        data = {'ingredient': 'test', 'unit': self.unit.pk}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        # why is 'ingredient': None allowed? Different error than required?
        self.assertContains(response, 'This field is required.')

    def test_form_is_shown(self):
        """
        Ensures that a form is shown to a user.

        NOTE: string may change, not the best practice to hard code it.
        """

        url = reverse('fridge:fridge_detail')
        response = self.client.get(url)

        self.assertContains(response, 'Add')


class FridgeDetailTests(TestCase):
    """ Test suite to ensure that fridge_detail template is correct. """

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.fridge = Fridge.objects.create(user=self.user)
        self.client = logged_in_client()
        self.url = reverse('fridge:fridge_detail')

    def test_fridge_has_add_recipe_link(self):
        """ Ensures a user sees link to add_recipe view. """

        response = self.client.get(self.url)
        expected_url = reverse('fridge:add_recipe')
        expected = f'<a href="{expected_url}">Add a recipe</a>'

        self.assertContains(response, expected, html=True)

    def test_user_access_shows_no_ingredients(self):
        """ Ensures that nothing is shown when fridge is empty. """

        response = self.client.get(self.url)

        self.assertContains(response, 'There are no ingredients')

    def test_user_access_shows_ingredients(self):
        """ Ensures that a user is shown contents of a fridge. """

        unit = Unit.objects.create(name='kilogram', abbrev='kg')
        ingredient = Ingredient.objects.create(name='test', type='Fruit')
        fi = FI.objects.create(fridge=self.fridge, quantity=1,
                               ingredient=ingredient, unit=unit)
        response = self.client.get(self.url)

        self.assertContains(response, ingredient.name)
        self.assertContains(response, ingredient.get_absolute_url())
        self.assertContains(response, fi.quantity)
        self.assertContains(response, fi.unit.abbrev)

    def test_shows_recipes(self):
        """
        Ensures that a user is shown recipes in the fridge. Also makes sure
        that two recipes with the same names are not duplicated.
        """

        r1 = Recipe.objects.create(author=self.user, title='test',
                                   description='test')
        r2 = Recipe.objects.create(author=self.user, title='test',
                                   description='test')
        self.fridge.recipes.add(r1)
        response = self.client.get(self.url)

        self.assertContains(response, r1.title)
        self.assertContains(response, r2.title)

    def test_same_names_allowed(self):
        """
        Ensure that recipes with the same names ARE allowed. It would be too
        restrictive to force users to come up with new names. Rather, slugs
        should differ (see next unit test).
        """

        Recipe.objects.create(author=self.user, title='test', description='tst')
        Recipe.objects.create(author=self.user, title='tst', description='test')
        recipes = Recipe.objects.all()

        self.assertTrue(len(recipes) == 2)

    def test_slugs_different_same_names(self):
        """ Ensures that recipes with the same names have different slugs. """

        r1 = Recipe.objects.create(author=self.user, title='test',
                                   description='test')
        r2 = Recipe.objects.create(author=self.user, title='test',
                                   description='test')

        self.assertNotEquals(r1.slug, r2.slug)

    def test_shows_remove_ingredient(self):
        """ Ensures that a template has a 'remove ingredient' link. """

        i1 = Ingredient.objects.create(name='test1', type='Fruit')
        unit = Unit.objects.create(name='kilogram', abbrev='kg')
        fi1 = FI.objects.create(fridge=self.fridge, unit=unit, ingredient=i1,
                                quantity=1)
        remove_url = reverse('fridge:remove_ingredient', kwargs={'pk': fi1.pk})
        expected_html = f'<a class="fridge-remove" href="{remove_url}">'
        response = self.client.get(self.url)

        self.assertContains(response, expected_html)

    def test_shows_remove_recipe(self):
        """ Ensures that a template shows a remove recipe function. """

        r1 = Recipe.objects.create(author=self.user, title='test',
                                   description='test')
        self.fridge.recipes.add(r1)
        response = self.client.get(self.url)
        remove_url = reverse('fridge:remove_recipe', kwargs={'pk': r1.pk})
        expected_href = f'<a class="fridge-remove" href="{remove_url}">'

        self.assertContains(response, expected_href)

    def test_shows_possibilities_link_in_template(self):
        """
        Ensures a link to possibilities view is references somewhere in the
        fridge.
        """

        i1 = Ingredient.objects.create(name='test1', type='Fruit')
        u = Unit.objects.create(name='kilogram', abbrev='kg')
        FI.objects.create(fridge=self.fridge, quantity=1, ingredient=i1, unit=u)

        response = self.client.get(self.url)
        expected_url = reverse('fridge:possibilities')
        expected_html = f'<a href="{expected_url}">Make something!</a>'

        self.assertContains(response, expected_html, html=True)

    def test_shows_fridge_recipes_link_in_template(self):
        """
        Ensures a link to possibilities view is references somewhere in the
        fridge.
        """

        i1 = Ingredient.objects.create(name='test1', type='Fruit')
        u = Unit.objects.create(name='kilogram', abbrev='kg')
        FI.objects.create(fridge=self.fridge, quantity=1, ingredient=i1, unit=u)

        response = self.client.get(self.url)
        expected_url = reverse('fridge:fridge_recipes')
        expected_html = f'<a href="{expected_url}">Make something I like!</a>'

        self.assertContains(response, expected_html, html=True)


class PossibilitiesTests(TestCase):
    """
    Test suite to ensure that possibilities template shows possible recipes.
    """

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        populate_fridge_ingredients()
        self.recipes = populate_recipes()
        self.client = logged_in_client()
        self.url = reverse('fridge:possibilities')

    def test_correct_template_used(self):
        """ Ensures the correct template is used. """

        response = self.client.get(self.url)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'fridge/possibilities.html')

    def test_recipes_are_shown(self):
        """ Ensures that possible global recipes are shown in the template. """

        response = self.client.get(self.url)
        expected_title = self.recipes[0].title
        expected_url = self.recipes[0].get_absolute_url()

        self.assertContains(response, expected_title, status_code=HTTPStatus.OK)
        self.assertContains(response, f'<a href="{expected_url}">')

    def test_fridge_recipes_not_shown_without_fridge_ingredients(self):
        """
        Ensures that global recipes are only shown when there are ingredients
        in a fridge.
        """

        FI.objects.all().delete()

        response = self.client.get(self.url)
        recipe_title = self.recipes[0].title

        self.assertNotContains(response, recipe_title)


class FridgeRecipesTests(TestCase):
    """
    Test suite to ensure that fridge_recipes template shows recipes from a
    fridge that can be made with given ingredients.
    """

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        populate_fridge_ingredients()
        self.recipes = list(populate_recipes())
        self.client = logged_in_client()
        self.url = reverse('fridge:fridge_recipes')

    def test_correct_template_used(self):
        """ Ensures the correct template is used. """

        response = self.client.get(self.url)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'fridge/fridge_recipes.html')

    def test_fridge_recipes_are_shown_except_those_not_in_fridge(self):
        """ Ensures that possible fridge recipes are shown in the template. """

        fridge = Fridge.objects.get(user=self.user)
        fridge.recipes.add(self.recipes[0])
        fridge.recipes.add(self.recipes[1])
        fridge.recipes.add(self.recipes[2])
        response = self.client.get(self.url)
        expected_title = self.recipes[3].title
        expected_url = self.recipes[3].get_absolute_url()
        expected_html = f'<a href={expected_url}>{expected_title}</a>'
        self.assertNotContains(response, expected_title, status_code=HTTPStatus.OK)
        self.assertNotContains(response, expected_html, html=True)

    def test_fridge_recipes_are_shown(self):
        """ Ensures that possible fridge recipes are shown in the template. """

        fridge = Fridge.objects.get(user=self.user)
        fridge.recipes.add(self.recipes[0])
        fridge.recipes.add(self.recipes[1])
        fridge.recipes.add(self.recipes[2])
        fridge.recipes.add(self.recipes[3])
        response = self.client.get(self.url)
        expected_title = self.recipes[0].title
        expected_url = self.recipes[0].get_absolute_url()
        expected_html = f'<a href="{expected_url}">'
        self.assertContains(response, expected_title, status_code=HTTPStatus.OK)
        self.assertContains(response, expected_html)

    def test_fridge_recipes_not_shown_without_fridge_ingredients(self):
        """
        Ensures that fridge recipes are only shown when there are ingredients
        in a fridge.
        """

        FI.objects.all().delete()

        response = self.client.get(self.url)
        recipe_title = self.recipes[0].title

        self.assertNotContains(response, recipe_title)