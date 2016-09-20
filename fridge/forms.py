from django.forms import ModelForm, Select, NumberInput

from .models import FridgeIngredient


class FridgeIngredientForm(ModelForm):
    """
    A form that is used to add ingredients to a fridge.

    Fridge is excluded from the form, as the form will be shown in a fridge
    view, hence a fridge is determined in there.

    Note that even though HTML5 validation for minimum numbers is employed,
    there is also a MinValueValidator in the FridgeIngredient model, to ensure
    that there is no situation where <0 value is provided.
    """

    class Meta:
        model = FridgeIngredient
        exclude = ("fridge", )

        widgets = {
            'ingredient': Select(attrs={'required': 'true'}),
            'unit': Select(attrs={'required': 'true'}),
            'quantity': NumberInput(attrs={'required': 'true', 'min': '0'})
        }
