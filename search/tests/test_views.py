from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse, resolve

from search.views import search_results


class ResultsViewTests(TestCase):
    """ Test suite to ensure main search view performs what it should. """

    def setUp(self):
        self.client = Client()
        self.url = reverse('search:search_results')

    def test_url_resolves_no_query(self):
        """ Ensures url can be accessed. """

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_url_correct_no_query(self):
        """ Ensures that url routes to a correct view. """

        resolver = resolve(self.url)

        self.assertEqual(resolver.view_name, 'search:search_results')
        self.assertEqual(resolver.func, search_results)

    def test_url_resolves_with_query(self):
        """ Ensures url can be accessed when the query is passed. """

        url = self.url + '?q=test'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

