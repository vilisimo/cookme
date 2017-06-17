from string import capwords

from http import HTTPStatus

from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from utilities.mock_db import populate_recipes


class SearchResultsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('search:search_results') + '?q='

        self.lemon = 'lemon'
        self.meat = 'meat'
        self.white_bread = 'white-bread'

    def test_one_ingredient_no_recipes_ingredient_still_shown(self):
        """
        Ensures that an ingredient is shown regardless whether a matching
        recipe is found or not. User should always know what was searched for.
        """

        url = self.url + self.lemon
        expected = capwords(self.lemon)
        
        response = self.client.get(url)

        self.assertContains(response, expected, status_code=HTTPStatus.OK)
        self.assertTemplateUsed('search/search_results.html')

    def test_one_ingredient_with_recipes(self):
        """
        Ensure that when there is a matching recipe, it's title is shown.
        """

        r = populate_recipes()[0]  #MeatRec
        url = self.url + self.meat
        response = self.client.get(url)
        expected_ingredient = capwords(self.meat)
        expected_recipe = r.title
        expected_url = f'<a href="{r.get_absolute_url()}">'

        self.assertContains(response, expected_ingredient, status_code=HTTPStatus.OK)
        self.assertContains(response, expected_recipe)
        self.assertContains(response, expected_url)

    def test_two_ingredients_one_with_dashes(self):
        """
        Ensure that ingredients that have spaces (encoded as dashes) are
        shown properly, and the recipes are displayed accordingly.
        """

        r = populate_recipes()[2]
        url = self.url + self.lemon + '+' + self.white_bread
        response = self.client.get(url)
        expected_ingredient = capwords(self.white_bread.replace('-', ' '))
        expected_recipe = r.title

        self.assertContains(response, expected_ingredient, status_code=HTTPStatus.OK)
        self.assertContains(response, expected_recipe)
