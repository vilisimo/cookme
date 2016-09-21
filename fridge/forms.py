from string import capwords

from django.forms import (
    ModelForm,
    Select,
    NumberInput,
    ModelChoiceField,
    CharField,
    TextInput,
)

from .models import FridgeIngredient
from ingredients.models import Ingredient, Unit


class FridgeIngredientForm(ModelForm):
    """
    A form that is used to add ingredients to a fridge.

    Fridge is excluded from the form, as the form will be shown in a fridge
    view, hence a fridge is determined in there.

    Note that even though HTML5 validation for minimum numbers is employed,
    and default value is always one of the existing models, there is also a
    MinValueValidator in the FridgeIngredient model, to ensure that there is
    no situation where <0 value is provided.
    """

    ingredient = CharField(widget=TextInput(
        attrs={'required': 'true', 'placeholder': 'Enter ingredient'})
    )
    unit = ModelChoiceField(Unit.objects.all(), empty_label=None)

    class Meta:
        model = FridgeIngredient
        exclude = ("fridge", "ingredient")

        widgets = {
            'unit': Select(attrs={'required': 'true'}),
            'quantity': NumberInput(attrs={'required': 'true', 'min': '0',
                                           'placeholder': 'Enter quantity'})
        }

    def save(self, commit=True):
        """
        Overrides the default save method, so that the user can enter an
        ingredient instead of searching through a list of them. While it
        opens up the database for potential errors, it allows for much more
        user-friendly experience, as well as more diverse ingredients.

        Of note: every ingredient starts with a capital letter, thus first
        letter is capitalized.
        """

        # Take the input string, create ingredient that has the same name.
        ingredient_name = capwords(self.cleaned_data['ingredient'])
        ing = Ingredient.objects.get_or_create(name=ingredient_name)[0]
        self.instance.ingredient = ing

        return super(FridgeIngredientForm, self).save(commit)
