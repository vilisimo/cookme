from django import forms
from django.forms import ModelForm, BaseFormSet
from django.utils.translation import gettext as _

from .models import RecipeIngredient, Recipe


class AddRecipeForm(ModelForm):
    """
    The form to create a recipe instance. That is, create a recipe and add it
    to a fridge. If user wants to add an exiting recipe to a fridge, he/she
    has to navigate to that fridge and click appropriate button.
    """

    class Meta:
        model = Recipe
        fields = ("title", "description", "steps", "cuisine", "image",)

        widgets = {
            'title': forms.TextInput(
                attrs={'placeholder': 'Recipe\'s title'}
            ),
            'description': forms.Textarea(
                attrs={'placeholder': 'Please provide a short description of '
                                      'the recipe.'}
            ),
            'steps': forms.Textarea(
                attrs={'placeholder': 'Please explain how to prepare a dish. '
                                      'Provide each step on a new line. '
                                      'Multiple new lines can be used.'}
            ),
            'cuisine': forms.Select(
                attrs={'required': 'true'}
            ),
        }

        labels = {
            'title': '',
            'description': '',
            'steps': '',
        }


class RecipeIngredientForm(ModelForm):
    """
    The form that is used to add associate an ingredient with a given recipe.
    Note that several of these forms must be used in order to add more than one
    ingredient. For this, JavaScript can be employed to create them on the fly.
    Also note that recipe is excluded: this is done so because recipe is not
    yet created, as the form is shown on the same page.
    """

    class Meta:
        model = RecipeIngredient
        exclude = ("recipe",)

        widgets = {
            'ingredient': forms.Select(attrs={'required': 'true'}),
            'unit': forms.Select(attrs={'required': 'true'}),
            'quantity': forms.NumberInput(attrs={'required': 'true'}),
        }


class BaseRecipeIngredientFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
        """
        Avoids the problem where the user may try to add a recipe & a formset
        without entering any value in ingredient form. If init is not overriden,
        then entering nothing does not catch errors.
        """

        super(BaseRecipeIngredientFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False

    def clean(self):
        """ Ensure that the same two ingredients cannot be chosen """

        if any(self.errors):
            return

        if not self.forms[0].has_changed():
            raise forms.ValidationError(_('Please add at least one field.'))

        ingredients = []
        for form in self.forms:
            ingredient = form.cleaned_data['ingredient']
            if ingredient in ingredients:
                raise forms.ValidationError(_("Ingredients should be "
                                              "distinct."))
            ingredients.append(ingredient)