"""
Test suite for views, urls.
"""


from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, resolve
from django.test.client import Client

from .models import Fridge
from .views import fridge_detail, add_recipe


def logged_in_client():
    """ Creates logged in user. """

    client = Client()
    client.login(username='test', password='test')
    return client


class AddRecipeTests(TestCase):
    """ Test suite to ensure that add_recipe view works correctly """

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


class FridgeDetailViewURLsTests(TestCase):
    """
    Test suite to check whether the views associated with Fridge model are
    functioning correctly. Includes tests on views and URLs.
    """

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.fridge = Fridge.objects.create(user=self.user)
        self.client = logged_in_client()

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


