""" Forms related to searching functions. """

from django import forms


class SearchForm(forms.Form):
    """
    Not the most complex form, but it may be expand in the future. E.g.,
    adding a choice field for searching either by ingredient or recipe name.
    """

    placeholder = 'Enter ingredients, separated by a comma'
    attributes = {
        'placeholder': placeholder,
        'autofocus': 'autofocus'
    }
    q = forms.CharField(max_length=500, min_length=1, required=True, strip=True,
                        widget=forms.TextInput(attrs=attributes))
