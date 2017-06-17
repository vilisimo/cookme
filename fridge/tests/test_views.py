from http import HTTPStatus

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
    def setUp(self):
        self.url = reverse('fridge:fridge_detail')
        self.user = User.objects.create_user(username='test', password='test')
        self.fridge = Fridge.objects.create(user=self.user)
        self.unit = Unit.objects.create(name='kilogram', abbrev='kg')
        self.client = logged_in_client()
        self.data = {'ingredient': 'test', 'unit': self.unit.pk, 'quantity': 1}

    def test_maps_to_correct_view(self):
        url = '/fridge/'

        path = resolve(url)

        self.assertEqual(path.view_name, 'fridge:fridge_detail')
        self.assertEqual(path.func, fridge_detail)

    def test_form_present(self):
        response = self.client.get(self.url)

        self.assertTrue(response.context['form'])

    def test_valid_form_accepted(self):
        response = self.client.post(self.url, self.data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.url)

    def test_form_ingredient_missing_no_redirect(self):
        self.data['ingredient'] = ''

        response = self.client.post(self.url, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_form_unit_missing_no_redirect(self):
        self.data['unit'] = ''

        response = self.client.post(self.url, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_quantity_missing_no_redirect(self):
        self.data['quantity'] = None

        response = self.client.post(self.url, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_ingredient_created_when_form_valid(self):
        name = 'test'
        response = self.client.post(self.url, self.data)
        self.assertTrue(response.status_code, HTTPStatus.FOUND)

        ingredient = Ingredient.objects.get(name=name.capitalize())
        self.assertTrue(ingredient)

    def test_ingredient_updated_when_form_valid(self):
        i = Ingredient.objects.create(name='test', description='test', type='Fruit')
        FridgeIngredient.objects.create(fridge=self.fridge, ingredient=i, unit=self.unit, quantity=1)

        self.client.post(self.url, self.data)
        fi = FridgeIngredient.objects.get(ingredient=i)

        self.assertEqual(fi.quantity, 2)

    def test_fridge_ingredient_created_when_form_valid(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

        fridge = Fridge.objects.get(user=self.user)
        ingredient = Ingredient.objects.get(name='Test')
        fi = FridgeIngredient.objects.get(fridge=fridge, ingredient=ingredient)

        self.assertTrue(fi)

    def test_user_access_allowed(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_fridge_created_when_user_accesses_view(self):
        Fridge.objects.all().delete()

        response = self.client.get(self.url)
        fridge = Fridge.objects.get(user=self.user)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(fridge)

    def test_fridge_created_when_homepage_visited(self):
        Fridge.objects.all().delete()

        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

        response = self.client.get(reverse('fridge:fridge_detail'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_anonymous_not_shown_fridge(self):
        cl = Client()
        redirect_string = '/accounts/login/?next=' + self.url

        response = cl.get(self.url)

        self.assertRedirects(response, redirect_string)


class RemoveRecipeTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.client = logged_in_client()
        self.fridge = Fridge.objects.create(user=self.user)
        self.r = Recipe.objects.create(author=self.user, title='test',
                                       description='test', steps='test')
        self.fridge.recipes.add(self.r)
        self.url = reverse('fridge:remove_recipe', kwargs={'pk': self.r.pk})

    def test_url_maps_to_view(self):
        url = f'/fridge/remove_recipe/{self.r.pk}/'

        resolver = resolve(url)

        self.assertEqual(resolver.view_name, 'fridge:remove_recipe')
        self.assertEqual(resolver.func, remove_recipe)

    def test_remove_can_be_accessed(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_anonymous_cannot_access_remove(self):
        client2 = Client()
        redirect_url = f'{reverse("login")}?next={self.url}'

        response = client2.get(self.url)

        self.assertRedirects(response, redirect_url)

    def test_recipe_removal(self):
        recipes = self.fridge.recipes.all()
        self.assertEqual(len(recipes), 1)

        self.client.get(self.url)
        recipes = self.fridge.recipes.all()

        self.assertFalse(recipes)

    def test_not_allowed_to_remove_other_users_ingredients(self):
        u2 = User.objects.create_user(username='test2', password='test2')
        c2 = Client()
        c2.login(username='test2', password='test2')
        f2 = Fridge.objects.create(user=u2)
        f2.recipes.add(self.r)

        response = c2.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

        u1recipes = self.fridge.recipes.all()
        self.assertEqual(len(u1recipes), 1)

        u2recipes = f2.recipes.all()
        self.assertFalse(u2recipes)

    def test_not_allowed_to_remove_non_existent_recipes(self):
        url = reverse('fridge:remove_recipe', kwargs={'pk': 9999})

        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)


class RemoveIngredientTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.client = logged_in_client()
        self.fridge = Fridge.objects.create(user=self.user)
        self.unit = Unit.objects.create(name='kg', abbrev='kg')
        self.i1 = Ingredient.objects.create(name='test1', type='Fruit')
        self.i2 = Ingredient.objects.create(name='test2', type='Fruit')
        self.fi1 = FridgeIngredient.objects.create(fridge=self.fridge, ingredient=self.i1,
                                                   unit=self.unit, quantity=1)
        self.fi2 = FridgeIngredient.objects.create(fridge=self.fridge, ingredient=self.i2,
                                                   unit=self.unit, quantity=1)

    def test_remove_ingredient_url_maps_to_view(self):
        url = f'/fridge/remove_ingredient/{self.i1.pk}/'

        resolver = resolve(url)

        self.assertEqual(resolver.view_name, 'fridge:remove_ingredient')
        self.assertEqual(resolver.func, remove_ingredient)

    def test_accessing_view_redirects(self):
        url = reverse('fridge:remove_ingredient', kwargs={'pk': self.fi1.pk})

        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_accessing_view_removes_ingredient(self):
        url = reverse('fridge:remove_ingredient', kwargs={'pk': self.fi1.pk})

        self.client.get(url)
        ingredients = FridgeIngredient.objects.all()

        self.assertEqual(len(ingredients), 1)

    def test_removing_ingredient_from_other_fridge_not_allowed(self):
        other_user = User.objects.create_user(username='other')
        other_fridge = Fridge.objects.create(user=other_user)
        fi3 = FridgeIngredient.objects.create(fridge=other_fridge, unit=self.unit, quantity=1,
                                              ingredient=self.i1)

        url = reverse('fridge:remove_ingredient', kwargs={'pk': fi3.pk})
        response = self.client.get(url)
        self.assertRedirects(response, reverse('home'), status_code=HTTPStatus.FOUND)

        ingredient = FridgeIngredient.objects.get(fridge=other_fridge)
        self.assertTrue(ingredient)

    def test_remove_non_existent_not_allowed(self):
        url = reverse('fridge:remove_ingredient', kwargs={'pk': 9999})

        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_anonymous_access_not_allowed(self):
        client = Client()
        url = reverse('fridge:remove_ingredient', kwargs={'pk': self.fi1.pk})

        response = client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_anonymous_remove_access_not_allowed(self):
        cl = Client()
        url = reverse('fridge:remove_ingredient', kwargs={'pk': self.i1.pk})
        redirect_string = '/accounts/login/?next=' + url

        response = cl.get(url)

        self.assertRedirects(response, redirect_string)


class AddRecipeViewTests(TestCase):
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

    def test_url_mapped_to_correct_view(self):
        path = resolve('/fridge/add_recipe/')

        self.assertEqual(path.view_name, 'fridge:add_recipe')
        self.assertEqual(path.func, add_recipe)

    def test_add_detail_view_access(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_add_detail_view_not_allowed_for_anonymous(self):
        response = Client().get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_add_detail_create_fridge_if_missing(self):
        Fridge.objects.all().delete()
        fridges = Fridge.objects.all()
        self.assertFalse(fridges)

        response = self.client.get(self.url)
        fridge = Fridge.objects.get(user=self.user)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(fridge)

    def test_correct_template_used(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, 'fridge/add_recipe.html')

    def test_correct_username_is_sent_to_template(self):
        response = self.client.get(self.url)

        self.assertEqual(response.context['user'], self.user)

    def test_add_recipe_form_is_sent(self):
        response = self.client.get(self.url)

        self.assertTrue(response.context['form'])


class TestAddRecipeForm(TestCase):
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

    def test_valid_form_post_creates_recipe(self):
        Recipe.objects.all().delete()

        self.client.post(self.url, self.valid_data)
        recipe = Recipe.objects.get(title=self.r_name)

        self.assertTrue(recipe)

    def test_form_valid_post_added_to_a_users_fridge(self):
        self.client.post(self.url, self.valid_data)
        fridge = Fridge.objects.get(user=self.user)
        recipe = Recipe.objects.get(title=self.r_name)
        recipes = fridge.recipes.all()

        self.assertIn(recipe, recipes)

    def test_form_valid_redirects(self):
        url = reverse('fridge:fridge_detail')

        response = self.client.post(self.url, self.valid_data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, url)

    def test_ingredients_added_to_recipe(self):
        self.client.post(self.url, self.valid_data)

        recipe = Recipe.objects.get(title=self.r_name)
        ingredients = recipe.ingredients.all()

        self.assertEqual(len(ingredients), 2)
        self.assertIn(self.test1, ingredients)
        self.assertIn(self.test2, ingredients)

    def test_add_ingredient_form_is_shown(self):
        response = self.client.get(self.url)

        self.assertTrue(response.context['formset'])

    def test_anonymous_post_valid_data_not_allowed(self):
        client = Client()
        redirect_url = '/accounts/login/?next=' + self.url

        response = client.post(self.url, self.valid_data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirect_url)


class FridgePossibilitiesTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.ingredients = populate_ingredients()
        populate_fridge_ingredients()
        self.recipes = list(populate_recipes())  # QuerySets are lazy
        self.client = logged_in_client()
        self.url = reverse('fridge:possibilities')

    def test_url_mapped_to_correct_view(self):
        url = '/fridge/possibilities/'
        path = resolve(url)

        self.assertEqual(path.view_name, 'fridge:possibilities')
        self.assertEqual(path.func, possibilities)

    def test_user_can_access_a_view(self):
        response = self.client.get(self.url)

        self.assertEquals(response.status_code, HTTPStatus.OK)

    def test_anonymous_user_access_not_allowed(self):
        redirect_url = f'{reverse("login")}?next={self.url}'

        response = Client().get(self.url)

        self.assertRedirects(response, redirect_url)

    def test_context_has_ingredients(self):
        ingredient_name = self.ingredients[0].name

        response = self.client.get(self.url)

        self.assertIn(ingredient_name, response.context['ingredients'])

    def test_context_has_all_recipes(self):
        response = self.client.get(self.url)

        self.assertEquals(list(self.recipes), list(response.context['recipes']))

    def test_context_does_not_have_novel_recipes(self):
        # Create a completely new recipe that has all ingredients and then
        # one original one. This recipe should never be in a list of returned
        # recipes, as it has one more ingredient than there are in the fridge.
        i = Ingredient.objects.create(name='test', type='Fruit')
        u = Unit.objects.create(name='litre', abbrev='l')
        r = Recipe.objects.create(author=self.user, title='test', description='test', steps='test')
        RI.objects.create(recipe=r, ingredient=i, unit=u, quantity=1)
        RI.objects.create(recipe=r, ingredient=self.ingredients[0], unit=u, quantity=1)
        RI.objects.create(recipe=r, ingredient=self.ingredients[1], unit=u, quantity=1)
        RI.objects.create(recipe=r, ingredient=self.ingredients[2], unit=u, quantity=1)
        RI.objects.create(recipe=r, ingredient=self.ingredients[3], unit=u,quantity=1)

        all_recipes = Recipe.objects.all()
        response = self.client.get(self.url)

        self.assertNotEquals(list(all_recipes), list(response.context['recipes']))
        self.assertEquals(self.recipes, list(response.context['recipes']))

    def test_no_ingredients_in_a_fridge(self):
        FridgeIngredient.objects.all().delete()

        response = self.client.get(self.url)

        self.assertFalse(response.context['recipes'])

    def test_recipes_without_missing_ingredient_are_shown(self):
        missing = self.ingredients[0]
        FridgeIngredient.objects.get(ingredient=missing).delete()
        all_recipes = Recipe.objects.all()

        response = self.client.get(self.url)

        self.assertNotEquals(list(all_recipes), list(response.context['recipes']))
        self.assertTrue(len(response.context['recipes']) == 1)


class FridgePossibilitiesWithFridgeRecipesTests(TestCase):
    """
    Test suite to ensure that the matching function only returns recipes that
    are in the fridge, as well as appropriately handles missing data.
    """

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.ingredients = populate_ingredients()
        populate_fridge_ingredients()
        self.recipes = list(populate_recipes())
        self.client = logged_in_client()
        self.url = reverse('fridge:fridge_recipes')

    def test_url_mapped_to_correct_view(self):
        url = '/fridge/fridge_recipes/'

        view = resolve(url)

        self.assertEqual(view.view_name, 'fridge:fridge_recipes')
        self.assertEqual(view.func, fridge_recipes)

    def test_anonymous_access_not_allowed(self):
        redirect_url = f'{reverse("login")}?next={self.url}'

        response = Client().get(self.url)

        self.assertRedirects(response, redirect_url)

    def test_logged_in_access_allowed(self):
        response = self.client.get(self.url)

        self.assertEquals(response.status_code, HTTPStatus.OK)

    def test_context_has_ingredients(self):
        ingredient_name = self.ingredients[0].name

        response = self.client.get(self.url)

        self.assertIn(ingredient_name, response.context['ingredients'])

    def test_no_fridge_recipes_then_nothing_returned(self):
        response = self.client.get(self.url)

        self.assertFalse(list(response.context['recipes']))

    def test_fridge_has_recipes(self):
        fridge = Fridge.objects.get(user=self.user)
        fridge.recipes.add(self.recipes[0])
        fridge.recipes.add(self.recipes[1])
        fridge.recipes.add(self.recipes[2])
        fridge.recipes.add(self.recipes[3])

        response = self.client.get(self.url)

        self.assertEquals(self.recipes, list(response.context['recipes']))

    def test_fridge_has_two_recipes(self):
        fridge = Fridge.objects.get(user=self.user)
        fridge.recipes.add(self.recipes[0])
        fridge.recipes.add(self.recipes[1])
        expected = [self.recipes[0], self.recipes[1]]

        response = self.client.get(self.url)

        self.assertNotEquals(self.recipes, list(response.context['recipes']))
        self.assertEquals(expected, list(response.context['recipes']))
