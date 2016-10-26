from django.test import TestCase

from search.forms import SearchForm


class SearchFormTests(TestCase):
    """ Test suite to ensure SearchForm is validating input, etc. """

    def test_empty_form(self):
        """ Ensures empty form is not allowed. """

        form = SearchForm(data={})

        self.assertFalse(form.is_valid(), "Form with no data was valid.")
        self.assertIn("This field is required", str(form['q'].errors))

    def test_non_empty_string_one_character(self):
        """ Ensures non-empty, 1 character string is allowed"""

        data = {'q': 'a'}
        form = SearchForm(data=data)

        self.assertTrue(form.is_valid(), "Form with 1 char was invalid.")

    def test_string_too_long(self):
        """ Ensures lengthy string is not allowed. """

        data = {'q': 'a'*501}
        form = SearchForm(data=data)

        self.assertFalse(form.is_valid(), "Form with 501 char was valid.")
        self.assertIn("Ensure this value has at most 500 characters",
                      str(form['q'].errors))

    def test_string_too_long_if_whitespaces_counted(self):
        """
        Ensures that the form is accepted if string length < 500 without
        whitespaces.
        """

        data = {'q': 'a'*499 + ' '*5}
        form = SearchForm(data=data)

        self.assertTrue(len(data['q']) > 500)
        self.assertTrue(form.is_valid(), "Form with whitespace length > 500 "
                                         "was valid.")

    def test_multiple_words(self):
        """ Ensures that entering multiple words do not result in an error. """

        data = {'q': 'multiple words'}
        form = SearchForm(data=data)

        self.assertTrue(form.is_valid(), "Multiple words were not allowed.")
