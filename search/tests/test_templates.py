from string import capwords

from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from search.views import search_results
from utilities.mock_db import populate_recipes


class SearchResultsTests(TestCase):
    """
    Test suite to ensure that essential information is shown in templates of
    any style.
    """

    def setUp(self):
        self.client = Client()
        self.url = reverse('search:search_results') + '?q='

        # Ingredients
        self.l = 'lemon'
        self.m = 'meat'
        self.b = 'white-bread'

    def test_one_ingredient_no_recipes(self):
        """
        Ensure that an ingredient is shown regardless whether a matching
        recipe is found.
        """

        url = self.url + self.l
        response = self.client.get(url)
        expected = capwords(self.l)

        self.assertContains(response, expected, status_code=200)
        self.assertTemplateUsed('search/search_results.html')

    def test_one_ingredient_with_recipes(self):
        """ Ensure that when there is a matching recipe, it is shown. """

        r = populate_recipes()[0]  #MeatRec
        url = self.url + self.m
        response = self.client.get(url)
        expected_ingredient = capwords(self.m)
        expected_recipe = r.title

        self.assertContains(response, expected_ingredient, status_code=200)
        self.assertContains(response, expected_recipe)

    def test_two_ingredients_one_with_dashes(self):
        """
        Ensure that ingredients that have spaces (encoded as dashes) are
        shown properly, and the recipes are displayed accordingly.
        """

        r = populate_recipes()[2]
        url = self.url + self.l + '+' + self.b
        response = self.client.get(url)
        expected_ingredient = capwords(self.b.replace('-', ' '))
        expected_recipe = r.title

        self.assertContains(response, expected_ingredient, status_code=200)
        self.assertContains(response, expected_recipe)
