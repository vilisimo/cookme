"""
Tests to ensure that helper functions are fully operational.
"""

from django.test import TestCase

from .helper_functions import generate_querystring


class QueryStringGenerationTests(TestCase):
    """
    Test suite to ensure that function producing query string functions
    properly.
    """

    def test_one_word(self):
        """ Ensures that one word query strings are constructed properly. """

        query = 'oneword'
        generated = generate_querystring(query)

        self.assertEqual(query, generated)

    def test_multiple_words(self):
        """ Ensures that multi-word queries are formatted properly. """

        query = "multiple words"
        generated = generate_querystring(query)
        query = query.replace(' ', '-')

        self.assertEqual(query, generated)

    def test_multiple_terms(self):
        """
        Ensures that multiple terms that may contain multi-word ingredients /
        recipes are formatted properly.

        Reminder: spaces between multi-word ingredients/recipes should be
        replaced by dashes.
        """

        query = "multiple words, ingredient, ingredient 2"
        expected = "multiple-words ingredient ingredient-2"
        generated = generate_querystring(query)

        self.assertEqual(expected, generated)

