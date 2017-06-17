from django.test import TestCase

from search.forms import SearchForm

max_chars = 500


class SearchFormTests(TestCase):
    def setUp(self):
        self.data = {'q': 'a'}

    def test_empty_form_not_allowed(self):
        form = SearchForm(data={})

        self.assertFalse(form.is_valid(), 'Form with no data was valid.')
        self.assertIn('This field is required', str(form['q'].errors))

    def test_non_empty_string_one_character_allowed(self):
        form = SearchForm(data=self.data)

        self.assertTrue(form.is_valid(), 'Form with 1 char was invalid.')

    def test_too_long_string_not_allowed(self):
        self.data['q'] = 'a' * (max_chars + 1)
        form = SearchForm(data=self.data)
        expected_error = 'Ensure this value has at most 500 characters'

        self.assertFalse(form.is_valid(), 'Form with 501 char was valid.')
        self.assertIn(expected_error, str(form['q'].errors))

    def test_string_whitespaces_trimmed(self):
        self.data['q'] = 'a' * (max_chars - 1) + ' ' * 5
        form = SearchForm(data=self.data)

        self.assertTrue(len(self.data['q']) > 500)
        self.assertTrue(form.is_valid(), 'Form with whitespace length > 500 was valid.')

    def test_multiple_words_are_ok(self):
        self.data['q'] = 'multiple words'
        form = SearchForm(data=self.data)

        self.assertTrue(form.is_valid(), 'Multiple words were not allowed.')
