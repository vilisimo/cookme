"""
Test suite for views, urls.
"""


from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, resolve
from django.test.client import Client

from recipes.models import Recipe
from ingredients.models import Ingredient, Unit
from .models import Fridge, FridgeIngredient
from .views import fridge_detail, add_recipe


def logged_in_client():
    """ Creates logged in user. """

    client = Client()
    client.login(username='test', password='test')
    return client


class AddRecipeTests(TestCase):
    """
    Test suite to ensure that add_recipe view works correctly. This includes
    both form for adding a recipe and formset for adding ingredients.
    """

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.client = logged_in_client()

    def test_correct_url_is_used(self):
        """ Ensures the user is routed to correct url. """

        path = resolve('/fridge/add_recipe/')

        self.assertEqual(path.view_name, 'fridge:add_recipe')
        self.assertEqual(path.func, add_recipe)

    def test_add_detail_view(self):
        """ Ensures that a user can access the view. """

        response = self.client.get(reverse('fridge:add_recipe'))

        self.assertEqual(response.status_code, 200)

    def test_add_detail_view_anon(self):
        """ Ensures that anonymous user cannot access the view. """

        response = Client().get(reverse('fridge:add_recipe'))

        self.assertEqual(response.status_code, 302)

    def test_fridge_exists(self):
        """
        Test the view when fridge already exists: when it does not need to be
        created. Checks whether correct fridge is retrieved and whether it is
        being used correctly in a view.
        """

        Fridge.objects.create(user=self.user)
        response = self.client.get(reverse('fridge:add_recipe'))

        self.assertEqual(response.status_code, 200)

    def test_add_detail_create_fridge_if_missing(self):
        """
        You cannot add a recipe to a fridge that is non-existent. Hence,
        trying to do so should create an empty fridge for a user (if it did
        not exist before). However, user can only ever have 1 fridge.
        """

        response = self.client.get(reverse('fridge:add_recipe'))
        fridges = Fridge.objects.get(user=self.user)

        self.assertEqual(response.status_code, 200)
        self.assertNotEquals(fridges, None)

    def test_correct_template_used(self):
        """ Ensures that a correct template is used. """

        response = self.client.get(reverse('fridge:add_recipe'))

        self.assertTemplateUsed(response, 'fridge/add_recipe.html')

    def test_correct_username_is_sent_to_template(self):
        """
        Ensures that a correct user instance is sent to a template. It is
        important for the auto-fill of forms (i.e. to determine recipe's
        ownership).
        """

        response = self.client.get(reverse('fridge:add_recipe'))

        self.assertEqual(response.context['user'], self.user)

    def test_add_recipe_form_is_sent(self):
        """ Ensures that a correct form is sent to a template """

        response = self.client.get(reverse('fridge:add_recipe'))

        self.assertNotEquals(response.context['form'], None)

    def test_form_valid_post(self):
        """
        Ensures that a model is created when a valid form is passed. Note
        that a test for invalid forms is provided in forms & templates tests.
        """

        potato = Ingredient.objects.create(name='Potato', type='Vegetable')
        tomato = Ingredient.objects.create(name='Tomato', type='Fruit')
        unit = Unit.objects.create(name='kilogram', abbrev='kg')
        data = {
            'title': 'test',
            'description': 'test',
            'steps': 'test',
            'cuisine': 'ot',
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '',
            'form-0-ingredient': str(potato.pk),
            'form-0-unit': str(unit.pk),
            'form-0-quantity': '1',
            'form-1-ingredient': str(tomato.pk),
            'form-1-unit': str(unit.pk),
            'form-1-quantity': '1',
        }

        self.client.post(reverse('fridge:add_recipe'), data)
        recipe = Recipe.objects.get(title='test')

        self.assertTrue(recipe)

    def test_form_valid_post_added_to_a_fridge(self):
        """
        Ensures that upon a creation a recipe is added to a fridge that
        belongs to a user that added the recipe.
        """

        potato = Ingredient.objects.create(name='Potato', type='Vegetable')
        tomato = Ingredient.objects.create(name='Tomato', type='Fruit')
        unit = Unit.objects.create(name='kilogram', abbrev='kg')
        data = {
            'title': 'test',
            'description': 'test',
            'steps': 'test',
            'cuisine': 'ot',
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '',
            'form-0-ingredient': str(potato.pk),
            'form-0-unit': str(unit.pk),
            'form-0-quantity': '1',
            'form-1-ingredient': str(tomato.pk),
            'form-1-unit': str(unit.pk),
            'form-1-quantity': '1',
        }

        self.client.post(reverse('fridge:add_recipe'), data)
        fridge = Fridge.objects.get(user=self.user)
        recipe = Recipe.objects.get(title='test')
        recipes = fridge.recipes.all()

        self.assertIn(recipe, recipes)

    def test_form_valid_redirects(self):
        """
        Ensures when a form is posted, user is redirected back to his/her
        fridge.
        """

        potato = Ingredient.objects.create(name='Potato', type='Vegetable')
        tomato = Ingredient.objects.create(name='Tomato', type='Fruit')
        unit = Unit.objects.create(name='kilogram', abbrev='kg')
        data = {
            'title': 'test',
            'description': 'test',
            'steps': 'test',
            'cuisine': 'ot',
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '',
            'form-0-ingredient': str(potato.pk),
            'form-0-unit': str(unit.pk),
            'form-0-quantity': '1',
            'form-1-ingredient': str(tomato.pk),
            'form-1-unit': str(unit.pk),
            'form-1-quantity': '1',
        }

        url = reverse('fridge:fridge_detail')
        response = self.client.post(reverse('fridge:add_recipe'), data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, url)

    def test_ingredients_added_to_recipe(self):
        """ Test to ensure that ingredients are added to the recipe """

        potato = Ingredient.objects.create(name='Potato', type='Vegetable')
        tomato = Ingredient.objects.create(name='Tomato', type='Fruit')
        unit = Unit.objects.create(name='kilogram', abbrev='kg')
        data = {
            'title': 'test',
            'description': 'test',
            'steps': 'test',
            'cuisine': 'ot',
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '',
            'form-0-ingredient': str(potato.pk),
            'form-0-unit': str(unit.pk),
            'form-0-quantity': '1',
            'form-1-ingredient': str(tomato.pk),
            'form-1-unit': str(unit.pk),
            'form-1-quantity': '1',
        }

        self.client.post(reverse('fridge:add_recipe'), data)

        recipe = Recipe.objects.get(title='test')
        ingredients = recipe.ingredients.all()

        self.assertEqual(len(ingredients), 2)
        self.assertIn(potato, ingredients)
        self.assertIn(tomato, ingredients)

    def test_add_ingredient_form_is_shown(self):
        """ Ensures that a correct form is sent to a template. """

        response = self.client.get(reverse('fridge:add_recipe'))

        self.assertNotEquals(response.context['formset'], None)


class FridgeDetailViewURLsTests(TestCase):
    """
    Test suite to check whether the views associated with Fridge model are
    functioning correctly. Includes tests on views and URLs.
    """

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.fridge = Fridge.objects.create(user=self.user)
        self.unit = Unit.objects.create(name='kilogram', abbrev='kg')
        self.client = logged_in_client()

    def test_form_present(self):
        """ Ensures that the form is passed to the template. """

        url = reverse('fridge:fridge_detail')
        response = self.client.get(url)

        self.assertTrue(response.context['form'])

    def test_form_valid(self):
        """ Ensure that filled in form is valid. """

        url = reverse('fridge:fridge_detail')
        data = {'ingredient': 'test', 'unit': self.unit.pk, 'quantity': 1}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, url)

    def test_form_invalid_no_redirect(self):
        """ Ensure that if form is invalid, user is not redirected. """

        url = reverse('fridge:fridge_detail')
        data = dict()
        data['ingredient'] = ''
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)

        data['ingredient'] = 'test'
        data['unit'] = ''
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)

        data['unit'] = self.unit.pk
        data['quantity'] = None
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)

    def test_form_valid_ingredient_created(self):
        """ Ensure that when form is valid, ingredient is created. """

        name = 'test'
        url = reverse('fridge:fridge_detail')
        data = {'ingredient': name, 'unit': self.unit.pk, 'quantity': 1}
        response = self.client.post(url, data)

        self.assertTrue(response.status_code, 302)

        ingredient = Ingredient.objects.get(name=name.capitalize())

        self.assertTrue(ingredient)

    def test_form_valid_ingredient_updated(self):
        """ Ensure that when ingredient already exists, quantity is updated. """

        name = 'Test'
        quantity = 1
        i = Ingredient.objects.create(name=name, description='test',
                                      type='Fruit')
        FridgeIngredient.objects.create(fridge=self.fridge, ingredient=i,
                                        unit=self.unit, quantity=quantity)
        url = reverse('fridge:fridge_detail')
        d = {'ingredient': name, 'unit': self.unit.pk, 'quantity': quantity}
        self.client.post(url, d)
        fi = FridgeIngredient.objects.get(ingredient=i)

        self.assertEqual(fi.quantity, quantity*2)

    def test_form_valid_fridge_ingredient_created(self):
        """ Ensure that when form is valid, FridgeIngredient is created. """

        name = 'Test'
        url = reverse('fridge:fridge_detail')
        data = {'ingredient': name, 'unit': self.unit.pk, 'quantity': 1}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)

        fi = FridgeIngredient.objects.get(fridge=Fridge.objects.get(
            user=self.user), ingredient=Ingredient.objects.get(name=name))

        self.assertTrue(fi)

    def test_url_resolves_to_detail_fridge(self):
        """ Ensures that URL resolves to a correct view function. """

        view = resolve('/fridge/')

        self.assertEqual(view.func, fridge_detail)

    def test_user_access(self):
        """ Ensures that a user is allowed to access the fridge. """

        response = self.client.get(reverse('fridge:fridge_detail'))

        self.assertEqual(response.status_code, 200)

    def test_fridge_created(self):
        """
        Ensures that a fridge is created for a user upon accessing the view -
        in case for one or another reason it was not created on the front
        page or upon login.
        """

        Fridge.objects.all().delete()

        response = self.client.get(reverse('fridge:fridge_detail'))
        fridge = Fridge.objects.get(user=self.user)

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(fridge, None)

    def test_user_access_no_fridge_homepage_first(self):
        """
        Ensures that if a user does not have a fridge and tries to access
        home page, a fridge will be created.
        """

        Fridge.objects.all().delete()

        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('fridge:fridge_detail'))
        self.assertEqual(response.status_code, 200)

    """ Needs a test with anonymous user: once logging in is implemented """
    # # Needs login page first, otherwise 404?
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


