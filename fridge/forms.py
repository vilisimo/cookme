from django import forms
from django.forms import ModelForm

from recipes.models import Recipe


class AddRecipeFridgeForm(ModelForm):
    """
    The form to create a recipe instance. That is, create a recipe and add it
    to a fridge. If user wants to add an exiting recipe to a fridge, he/she
    has to navigate to that fridge and click appropriate button.
    """

    class Meta:
        model = Recipe
        fields = ("title", "description", "image", )

        widgets = {
            'title': forms.TextInput(
                attrs={'placeholder': 'Recipe\'s title'}),
            'description': forms.Textarea(
                attrs={'placeholder': 'Please explain how to prepare a dish, '
                                      'and upload a photo of a finished '
                                      'product'})
        }

        labels = {
            'title': '',
            'description': '',
            'image': '',
        }
