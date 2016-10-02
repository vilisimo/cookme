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
from .views import fridge_detail, add_recipe, remove_ingredient, remove_recipe


def logged_in_client():
    """ Creates logged in user. """

    client = Client()
    client.login(username='test', password='test')
    return client


class RemoveRecipeTests(TestCase):
    """
    Test suite to ensure that a recipe in a fridge can be removed properly.
    """

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.client = logged_in_client()
        self.fridge = Fridge.objects.create(user=self.user)
        self.r = Recipe.objects.create(author=self.user, title='test',
                                       description='test', steps='test')
        self.fridge.recipes.add(self.r)
        self.url = reverse('fridge:remove_recipe', kwargs={'pk': self.r.pk})

    def test_url_route(self):
        """ Ensures that URL routes to correct view. """

        url = '/fridge/remove_recipe/{}/'.format(self.r.pk)
        resolver = resolve(url)

        self.assertEqual(resolver.view_name, 'fridge:remove_recipe')
        self.assertEqual(resolver.func, remove_recipe)

    def test_access_remove_recipe_view(self):
        """ Ensures that a user can access a view and is redirected. """

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)

    def test_anonymous_access_remove_recipe_view(self):
        """ Ensures anonymous users cannot access the view. """

        client2 = Client()
        response = client2.get(self.url)
        redirect_url = '{}?next={}'.format(reverse('login'), self.url)

        self.assertRedirects(response, redirect_url)

    def test_recipe_removal(self):
        """ Ensures a recipe can be removed. """

        recipes = self.fridge.recipes.all()

        self.assertEqual(len(recipes), 1)

        self.client.get(self.url)
        recipes = self.fridge.recipes.all()

        self.assertFalse(recipes)

    def test_different_user_removal(self):
        """
        Ensures that a particular user cannot remove ingredient from other
        people's fridge.
        """

        u2 = User.objects.create_user(username='test2', password='test2')
        c2 = Client()
        c2.login(username='test2', password='test2')
        f2 = Fridge.objects.create(user=u2)
        f2.recipes.add(self.r)

        response = c2.get(self.url)

        self.assertEqual(response.status_code, 302)

        u1recipes = self.fridge.recipes.all()

        self.assertEqual(len(u1recipes), 1)

        u2recipes = f2.recipes.all()

        self.assertFalse(u2recipes)

    def test_remove_non_existent(self):
        """
        Ensures non-existent recipes cannot be removed and an error is thrown.
        """

        url = reverse('fridge:remove_recipe', kwargs={'pk': 9999})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)


class RemoveIngredientTests(TestCase):
    """ 
    Test suite to ensure that a view for ingredient removal works correctly.
    """

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.client = logged_in_client()
        self.fridge = Fridge.objects.create(user=self.user)
        self.unit = Unit.objects.create(name='kg', abbrev='kg')
        self.i1 = Ingredient.objects.create(name='test1', type='Fruit')
        self.i2 = Ingredient.objects.create(name='test2', type='Fruit')
        self.fi1 = FridgeIngredient.objects.create(fridge=self.fridge,
                                                   ingredient=self.i1,
                                                   unit=self.unit,
                                                   quantity=1)
        self.fi2 = FridgeIngredient.objects.create(fridge=self.fridge,
                                                   ingredient=self.i2,
                                                   unit=self.unit,
                                                   quantity=1)

    def test_url_route_remove_ingredient(self):
        """ Ensures that URL routes to correct view. """

        url = '/fridge/remove_ingredient/{}/'.format(self.i1.pk)
        resolver = resolve(url)

        self.assertEqual(resolver.view_name, 'fridge:remove_ingredient')
        self.assertEqual(resolver.func, remove_ingredient)

    def test_access_view_successful(self):
        """ Ensure that upon accessing a view, user is redirected. """

        url = reverse('fridge:remove_ingredient', kwargs={'pk': self.fi1.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

    def test_access_view_ingredient_removed(self):
        """ Ensure that ingredient is removed after accessing the view. """

        url = reverse('fridge:remove_ingredient', kwargs={'pk': self.fi1.pk})
        self.client.get(url)
        ingredients = FridgeIngredient.objects.all()

        self.assertEqual(len(ingredients), 1)

    def test_remove_ingredient_from_other_fridge(self):
        """ Ensure that ingredients from other fridges cannot be removed. """

        other_user = User.objects.create_user(username='other')
        other_fridge = Fridge.objects.create(user=other_user)
        fi3 = FridgeIngredient.objects.create(fridge=other_fridge,
                                              unit=self.unit,
                                              quantity=1, ingredient=self.i1)

        url = reverse('fridge:remove_ingredient', kwargs={'pk': fi3.pk})
        response = self.client.get(url)

        self.assertRedirects(response, reverse('home'), status_code=302)

        ingredient = FridgeIngredient.objects.get(fridge=other_fridge)

        self.assertTrue(ingredient)

    def test_remove_non_existent(self):
        """
        Ensures that trying to remove non-existent ingredient throws 404.
        """

        url = reverse('fridge:remove_ingredient', kwargs={'pk': 9999})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_access_view_anonymous(self):
        """ Test to ensure that non-logged in people cannot access the view. """

        client = Client()
        url = reverse('fridge:remove_ingredient', kwargs={'pk': self.fi1.pk})
        response = client.get(url)

        self.assertEqual(response.status_code, 302)

    # Needs login page first, otherwise 404?
    def test_anonymous_remove_access(self):
        """ Test to ensure that the anonymous user is not shown a fridge """

        cl = Client()

        url = reverse('fridge:remove_ingredient', kwargs={'pk': self.i1.pk})
        redirect_string = '/accounts/login/?next='
        response = cl.get(url)

        self.assertRedirects(response, redirect_string + url)


class AddRecipeTests(TestCase):
    """
    Test suite to ensure that add_recipe view works correctly. This includes
    both form for adding a recipe and formset for adding ingredients.
    """

    def setUp(self):
        self.url = reverse('fridge:add_recipe')
        self.user = User.objects.create_user(username='test', password='test')
        self.client = logged_in_client()
        self.r_name = 'Test'
        self.test1 = Ingredient.objects.create(name='Potato', type='Vegetable')
        self.test2 = Ingredient.objects.create(name='Tomato', type='Fruit')
        self.unit = Unit.objects.create(name='kilogram', abbrev='kg')
        self.valid_data = {
            'title': 'test',
            'description': self.r_name,
            'steps': 'test',
            'cuisine': 'ot',
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '',
            'form-0-ingredient': 'Potato',
            'form-0-unit': str(self.unit.pk),
            'form-0-quantity': '1',
            'form-1-ingredient': 'Tomato',
            'form-1-unit': str(self.unit.pk),
            'form-1-quantity': '1',
        }

    def test_correct_url_is_used(self):
        """ Ensures the user is routed to correct url. """

        path = resolve('/fridge/add_recipe/')

        self.assertEqual(path.view_name, 'fridge:add_recipe')
        self.assertEqual(path.func, add_recipe)

    def test_add_detail_view(self):
        """ Ensures that a user can access the view. """

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_add_detail_view_anon(self):
        """ Ensures that anonymous user cannot access the view. """

        response = Client().get(self.url)

        self.assertEqual(response.status_code, 302)

    def test_fridge_exists(self):
        """
        Test the view when fridge already exists: when it does not need to be
        created. Checks whether correct fridge is retrieved and whether it is
        being used correctly in a view.
        """

        Fridge.objects.create(user=self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_add_detail_create_fridge_if_missing(self):
        """
        You cannot add a recipe to a fridge that is non-existent. Hence,
        trying to do so should create an empty fridge for a user (if it did
        not exist before). However, user can only ever have 1 fridge.
        """

        response = self.client.get(self.url)
        fridges = Fridge.objects.get(user=self.user)

        self.assertEqual(response.status_code, 200)
        self.assertNotEquals(fridges, None)

    def test_correct_template_used(self):
        """ Ensures that a correct template is used. """

        response = self.client.get(self.url)

        self.assertTemplateUsed(response, 'fridge/add_recipe.html')

    def test_correct_username_is_sent_to_template(self):
        """
        Ensures that a correct user instance is sent to a template. It is
        important for the auto-fill of forms (i.e. to determine recipe's
        ownership).
        """

        response = self.client.get(self.url)

        self.assertEqual(response.context['user'], self.user)

    def test_add_recipe_form_is_sent(self):
        """ Ensures that a correct form is sent to a template """

        response = self.client.get(self.url)

        self.assertNotEquals(response.context['form'], None)

    def test_form_valid_post(self):
        """
        Ensures that a model is created when a valid form is passed. Note
        that a test for invalid forms is provided in forms & templates tests.
        """

        self.client.post(self.url, self.valid_data)
        recipe = Recipe.objects.get(title=self.r_name)

        self.assertTrue(recipe)

    def test_form_valid_post_added_to_a_fridge(self):
        """
        Ensures that upon a creation a recipe is added to a fridge that
        belongs to a user that added the recipe.
        """

        self.client.post(self.url, self.valid_data)
        fridge = Fridge.objects.get(user=self.user)
        recipe = Recipe.objects.get(title=self.r_name)
        recipes = fridge.recipes.all()

        self.assertIn(recipe, recipes)

    def test_form_valid_redirects(self):
        """
        Ensures when a form is posted, user is redirected back to his/her
        fridge.
        """

        url = reverse('fridge:fridge_detail')
        response = self.client.post(self.url, self.valid_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, url)

    def test_ingredients_added_to_recipe(self):
        """ Test to ensure that ingredients are added to the recipe """

        self.client.post(self.url, self.valid_data)

        recipe = Recipe.objects.get(title=self.r_name)
        ingredients = recipe.ingredients.all()

        self.assertEqual(len(ingredients), 2)
        self.assertIn(self.test1, ingredients)
        self.assertIn(self.test2, ingredients)

    def test_add_ingredient_form_is_shown(self):
        """ Ensures that a correct form is sent to a template. """

        response = self.client.get(self.url)

        self.assertNotEquals(response.context['formset'], None)

    def test_anonymous_post_valid_data(self):
        """
        Ensures that anonymous users cannot post data without logging in.
        """

        client = Client()
        redirect_url = '/accounts/login/?next='
        response = client.post(self.url, self.valid_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url + self.url)


class FridgeDetailViewURLsTests(TestCase):
    """
    Test suite to check whether the views associated with Fridge model are
    functioning correctly. Includes tests on views and URLs.
    """

    def setUp(self):
        self.url = reverse('fridge:fridge_detail')
        self.user = User.objects.create_user(username='test', password='test')
        self.fridge = Fridge.objects.create(user=self.user)
        self.unit = Unit.objects.create(name='kilogram', abbrev='kg')
        self.client = logged_in_client()

    def test_correct_view(self):
        """ Ensures that url is connected to a correct view. """

        url = '/fridge/'
        path = resolve(url)

        self.assertEqual(path.view_name, 'fridge:fridge_detail')
        self.assertEqual(path.func, fridge_detail)

    def test_form_present(self):
        """ Ensures that the form is passed to the template. """

        response = self.client.get(self.url)

        self.assertTrue(response.context['form'])

    def test_form_valid(self):
        """ Ensure that filled in form is valid. """

        data = {'ingredient': 'test', 'unit': self.unit.pk, 'quantity': 1}
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.url)

    def test_form_invalid_no_redirect(self):
        """ Ensure that if form is invalid, user is not redirected. """

        data = dict()
        data['ingredient'] = ''
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 200)

        data['ingredient'] = 'test'
        data['unit'] = ''
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 200)

        data['unit'] = self.unit.pk
        data['quantity'] = None
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 200)

    def test_form_valid_ingredient_created(self):
        """ Ensure that when form is valid, ingredient is created. """

        name = 'test'
        data = {'ingredient': name, 'unit': self.unit.pk, 'quantity': 1}
        response = self.client.post(self.url, data)

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
        d = {'ingredient': name, 'unit': self.unit.pk, 'quantity': quantity}
        self.client.post(self.url, d)
        fi = FridgeIngredient.objects.get(ingredient=i)

        self.assertEqual(fi.quantity, quantity*2)

    def test_form_valid_fridge_ingredient_created(self):
        """ Ensure that when form is valid, FridgeIngredient is created. """

        name = 'Test'
        data = {'ingredient': name, 'unit': self.unit.pk, 'quantity': 1}
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 302)

        fi = FridgeIngredient.objects.get(fridge=Fridge.objects.get(
            user=self.user), ingredient=Ingredient.objects.get(name=name))

        self.assertTrue(fi)

    def test_user_access(self):
        """ Ensures that a user is allowed to access the fridge. """

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_fridge_created(self):
        """
        Ensures that a fridge is created for a user upon accessing the view -
        in case for one or another reason it was not created on the front
        page or upon login.
        """

        Fridge.objects.all().delete()

        response = self.client.get(self.url)
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

    def test_anonymous_access(self):
        """ Test to ensure that the anonymous user is not shown a fridge """

        cl = Client()

        redirect_string = '/accounts/login/?next='
        response = cl.get(self.url)

        self.assertRedirects(response, redirect_string + self.url)


