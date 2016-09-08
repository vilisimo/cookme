from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test.client import Client


###################################
""" Test Views, URLS & Templates"""
###################################


class HomePageTestCase(TestCase):
    """ Test suite to ensure that home page functions properly """

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.logged = Client()
        self.logged.login(username='test', password='test')

    def test_anonymous_visit(self):
        """ Test to ensure anonymous users do not see link to a fridge """

        response = Client().get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Fridge')

    def test_logged_visit(self):
        """ Test to ensure that logged in user sees the fridge """

        response = self.logged.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Fridge')
