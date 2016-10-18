from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse, resolve

from .views import results


class ResultsViewTests(TestCase):
    """ Test suite to ensure main search view performs what it should. """

    def setUp(self):
        self.client = Client()
        self.url = reverse('search:results')

    def test_url_resolves(self):
        """ Ensures url can be accessed. """

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_url_correct(self):
        """ Ensures that url routes to a correct view. """

        resolver = resolve(self.url)

        self.assertEqual(resolver.view_name, 'search:results')
        self.assertEqual(resolver.func, results)
