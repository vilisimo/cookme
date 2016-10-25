"""
Tests to ensure that helper functions are fully operational.
"""

from django.test import TestCase

from .helpers import encode, decode, get_name_set


class EncodingTests(TestCase):
    """
    Test suite to ensure that function producing query string functions
    properly.
    """

    def test_one_word(self):
        """ Ensures that one word query strings are constructed properly. """

        query = 'oneword'
        generated = encode(query)

        self.assertEqual(query, generated)

    def test_multiple_words(self):
        """ Ensures that multi-word queries are formatted properly. """

        query = "multiple words"
        generated = encode(query)
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
        generated = encode(query)

        self.assertEqual(expected, generated)


class DecodingTests(TestCase):
    """
    Test suite to ensure that decoding of query strings produces a correct
    result.
    """

    def test_one_word(self):
        """ Ensures that decoding does not mess up one word queries. """

        query = 'oneword'
        decoded = decode(query)

        self.assertEqual(query, decoded)

    def test_multiple_words(self):
        """ Ensures that decoding does not mess up multi-word queries. """

        query = 'multiple words'
        encoded = encode(query)
        decoded = decode(encoded)

        self.assertEqual(query, decoded)

    def test_multiple_terms(self):
        """
        Ensures that decoding does not mess up queries with multiple terms.

        Note that the space removal after comma is intentional. It is the
        expected functionality of decode function, as it makes processing
        later easier.
        """

        query = "multiple words, ingredient, ingredient 2"
        encoded = encode(query)
        decoded = decode(encoded)

        self.assertEqual(query.replace(', ', ','), decoded)


class GetNameSetExtractionTests(TestCase):
    """
    Test suite to ensure that a set of names extracted from decoding query is
    correct.
    """

    def test_one(self):
        """ Ensures that one word query results in a correct set. """

        query = 'oneword'
        encoded = encode(query)
        decoded = decode(encoded)
        names = get_name_set(decoded)
        expected = {'Oneword'}

        self.assertEqual(names, expected)

    def test_multiple_words(self):
        """ Ensures that processing multi-word queries returns a correct set """

        query = 'multi word'
        encoded = encode(query)
        decoded = decode(encoded)
        names = get_name_set(decoded)
        expected = {'Multi Word'}

        self.assertEqual(names, expected)

    def test_multiple_terms(self):
        """
        Ensures that processing a query with multiple terms returns a correct
        set.
        """

        query = 'multiple words, ingredient, ingredient 2'
        encoded = encode(query)
        decoded = decode(encoded)
        names = get_name_set(decoded)
        expected = {'Multiple Words', 'Ingredient', 'Ingredient 2'}

        self.assertEqual(names, expected)
