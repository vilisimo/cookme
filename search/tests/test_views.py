from http import HTTPStatus

from django.core.urlresolvers import reverse, resolve
from django.test import TestCase
from django.test.client import Client

from search.views import search_results


class ResultsViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('search:search_results')

    def test_url_resolves_no_query(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_url_correct_with_no_query(self):
        resolver = resolve(self.url)

        self.assertEqual(resolver.view_name, 'search:search_results')
        self.assertEqual(resolver.func, search_results)

    def test_url_resolves_with_query(self):
        url = self.url + '?q=test'
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
