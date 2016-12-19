"""
Test suite for fridge views, urls.
"""

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, resolve
from django.test import TestCase
from django.test.client import Client

from fridge.models import Fridge, FridgeIngredient
from fridge.views import (
    fridge_detail,
    add_recipe,
    remove_ingredient,
    remove_recipe,
    possibilities,
    fridge_recipes,
)
from ingredients.models import Ingredient, Unit
from recipes.models import Recipe, RecipeIngredient as RI
from utilities.mock_db import (
    logged_in_client, populate_ingredients, populate_fridge_ingredients,
    populate_recipes,
)


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
        self.data = {'ingredient': 'test', 'unit': self.unit.pk, 'quantity': 1}

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

        response = self.client.post(self.url, self.data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.url)

    def test_form_ingredient_missing_no_redirect(self):
        """ Ensure that if form is invalid, user is not redirected. """

        self.data['ingredient'] = ''
        response = self.client.post(self.url, self.data)

        self.assertEqual(response.status_code, 200)

    def test_form_unit_missing_no_redirect(self):
        """ Ensure that if a unit field is missing, user is not redirected. """

        self.data['unit'] = ''
        response = self.client.post(self.url, self.data)

        self.assertEqual(response.status_code, 200)

    def test_quantity_missing_no_redirect(self):
        """
        Ensure that if a quantity field is missing, user is not redirected.
        """

        self.data['quantity'] = None
        response = self.client.post(self.url, self.data)

        self.assertEqual(response.status_code, 200)

    def test_form_valid_ingredient_created(self):
        """ Ensure that when form is valid, ingredient is created. """

        name = 'test'
        response = self.client.post(self.url, self.data)
        self.assertTrue(response.status_code, 302)

        ingredient = Ingredient.objects.get(name=name.capitalize())
        self.assertTrue(ingredient)

    def test_form_valid_ingredient_updated(self):
        """ Ensure that when ingredient already exists, quantity is updated. """

        quantity = 1
        i = Ingredient.objects.create(name='test', description='test',
                                      type='Fruit')
        FridgeIngredient.objects.create(fridge=self.fridge, ingredient=i,
                                        unit=self.unit, quantity=quantity)
        self.client.post(self.url, self.data)
        fi = FridgeIngredient.objects.get(ingredient=i)

        self.assertEqual(fi.quantity, quantity*2)

    def test_form_valid_fridge_ingredient_created(self):
        """ Ensure that when form is valid, FridgeIngredient is created. """

        name = 'Test'
        response = self.client.post(self.url, self.data)

        self.assertEqual(response.status_code, 302)

        fridge = Fridge.objects.get(user=self.user)
        ingredient = Ingredient.objects.get(name=name)
        fi = FridgeIngredient.objects.get(fridge=fridge, ingredient=ingredient)

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
        """ Test to ensure that the anonymous user is not shown a fridge. """

        cl = Client()

        redirect_string = '/accounts/login/?next=' + self.url
        response = cl.get(self.url)

        self.assertRedirects(response, redirect_string)


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
                                              quantity=1,
                                              ingredient=self.i1)

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

    def test_anonymous_remove_access(self):
        """ Test to ensure that the anonymous user is not shown a fridge """

        cl = Client()

        url = reverse('fridge:remove_ingredient', kwargs={'pk': self.i1.pk})
        redirect_string = '/accounts/login/?next=' + url
        response = cl.get(url)

        self.assertRedirects(response, redirect_string)


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
        self.assertTrue(fridges)

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

        self.assertTrue(response.context['form'])

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

        self.assertTrue(response.context['formset'])

    def test_anonymous_post_valid_data(self):
        """
        Ensures that anonymous users cannot post data without logging in.
        """

        client = Client()
        redirect_url = '/accounts/login/?next=' + self.url
        response = client.post(self.url, self.valid_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)


class FridgePossibilitiesTests(TestCase):
    """
    Test suite to ensure that a user can access a view that shows possible
    recipes that he/she can make from ingredients in the fridge.
    """

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.ingredients = populate_ingredients()
        populate_fridge_ingredients()
        self.recipes = list(populate_recipes())  # QuerySets are lazy
        self.client = logged_in_client()
        self.url = reverse('fridge:possibilities')

    def test_correct_view(self):
        """ Ensures that url is connected to a correct view. """

        url = '/fridge/possibilities/'
        path = resolve(url)

        self.assertEqual(path.view_name, 'fridge:possibilities')
        self.assertEqual(path.func, possibilities)

    def test_user_can_access_a_view(self):
        """ Ensures a view can be accessed by a registered user. """

        response = self.client.get(self.url)

        self.assertEquals(response.status_code, 200)

    def test_anonymous_user_access(self):
        """ Ensures anonymous users cannot access this view. """

        response = Client().get(self.url)
        redirect_url = '{}?next={}'.format(reverse('login'), self.url)

        self.assertRedirects(response, redirect_url)

    def test_context_has_ingredients(self):
        """
        Ensures the ingredients are successfully retrieved from DB.
        Prerequisite for matching them against recipes.
        """

        ingredient_name = self.ingredients[0].name
        response = self.client.get(self.url)

        self.assertIn(ingredient_name, response.context['ingredients'])

    def test_context_has_all_recipes(self):
        """
        Context should have all 4 recipes, since populate_ingredients()
        creates all ingredients from which recipes are made.
        """

        response = self.client.get(self.url)

        self.assertEquals(list(self.recipes), list(response.context['recipes']))

    def test_context_does_not_have_novel_recipes(self):
        """
        Context should not have the fifth, novel recipe with novel ingredients
        that are not in the fridge.
        """

        # Create a completely new recipe that has all ingredients and then
        # one original one. This recipe should never be in a list of returned
        # recipes, as it has one more ingredient than there are in the fridge.
        i = Ingredient.objects.create(name='test', type='Fruit')
        u = Unit.objects.create(name='litre', abbrev='l')
        r = Recipe.objects.create(author=self.user, title='test',
                                  description='test', steps='test')
        RI.objects.create(recipe=r, ingredient=i, unit=u, quantity=1)
        RI.objects.create(recipe=r, ingredient=self.ingredients[0], unit=u,
                          quantity=1)
        RI.objects.create(recipe=r, ingredient=self.ingredients[1], unit=u,
                          quantity=1)
        RI.objects.create(recipe=r, ingredient=self.ingredients[2], unit=u,
                          quantity=1)
        RI.objects.create(recipe=r, ingredient=self.ingredients[3], unit=u,
                          quantity=1)

        all_rec = Recipe.objects.all()
        response = self.client.get(self.url)

        self.assertNotEquals(list(all_rec), list(response.context['recipes']))
        self.assertEquals(self.recipes, list(response.context['recipes']))

    def test_no_ingredients_in_a_fridge(self):
        """
        Ensure that when no ingredients are in a fridge, no recipes are
        returned.
        """

        FridgeIngredient.objects.all().delete()
        response = self.client.get(self.url)

        self.assertFalse(response.context['recipes'])

    def test_one_ingredient_missing(self):
        """
        Ensures that when one ingredient is missing from a fridge,
        only recipes without that ingredient are shown.

        Note: if we delete ingredient[0] (meat), only 1 recipe remains possible.
        """

        ingredient = self.ingredients[0]
        FridgeIngredient.objects.get(ingredient=ingredient).delete()
        all_rec = Recipe.objects.all()
        response = self.client.get(self.url)

        self.assertNotEquals(list(all_rec), list(response.context['recipes']))
        self.assertTrue(len(response.context['recipes']) == 1)


class FridgePossibilitiesWithFridgeRecipesTests(TestCase):
    """
    Test suite to ensure that the matching function only returns recipes that
    are in the fridge, as well as appropriately handles missing data and so on.
    """

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.ingredients = populate_ingredients()
        populate_fridge_ingredients()
        self.recipes = list(populate_recipes())
        self.client = logged_in_client()
        self.url = reverse('fridge:fridge_recipes')

    def test_correct_view(self):
        """ Ensures correct view is shown when url is accessed. """

        url = '/fridge/fridge_recipes/'
        view = resolve(url)

        self.assertEqual(view.view_name, 'fridge:fridge_recipes')
        self.assertEqual(view.func, fridge_recipes)

    def test_anonymous_access(self):
        """ Ensures anonymous user cannot access the view. """

        response = Client().get(self.url)
        redirect_url = '{}?next={}'.format(reverse('login'), self.url)

        self.assertRedirects(response, redirect_url)

    def test_logged_in_access(self):
        """ Ensures logged in user can access the view. """

        response = self.client.get(self.url)

        self.assertEquals(response.status_code, 200)

    def test_context_has_ingredients(self):
        """
        Ensures the ingredients are successfully retrieved from DB.
        Prerequisite for matching them against recipes.
        """

        ingredient_name = self.ingredients[0].name
        response = self.client.get(self.url)

        self.assertIn(ingredient_name, response.context['ingredients'])

    def test_no_fridge_recipes(self):
        """
        Ensures that when there are no recipes in the fridge, nothing is
        returned.
        """

        response = self.client.get(self.url)

        self.assertFalse(list(response.context['recipes']))

    def test_fridge_has_recipes(self):
        """
        Ensures that when fridge does have recipes, they are matched against
        ingredients.
        """

        fridge = Fridge.objects.get(user=self.user)
        fridge.recipes.add(self.recipes[0])
        fridge.recipes.add(self.recipes[1])
        fridge.recipes.add(self.recipes[2])
        fridge.recipes.add(self.recipes[3])
        response = self.client.get(self.url)

        self.assertEquals(self.recipes, list(response.context['recipes']))

    def test_fridge_has_two_recipes(self):
        """
        Ensures that when fridge has only some recipes, only those recipes in
        the fridge are matched against the ingredients.
        """

        fridge = Fridge.objects.get(user=self.user)
        fridge.recipes.add(self.recipes[0])
        fridge.recipes.add(self.recipes[1])
        expected = [self.recipes[0], self.recipes[1]]
        response = self.client.get(self.url)

        self.assertNotEquals(self.recipes, list(response.context['recipes']))
        self.assertEquals(expected, list(response.context['recipes']))
