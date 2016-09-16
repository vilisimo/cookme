from django import forms
from django.forms import ModelForm, BaseFormSet
from django.utils.translation import gettext as _

from ingredients.models import Ingredient, Unit
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
        # Need to make this appear in pop-up box upon clicking a field and
        # not doing anything for a few seconds.
        help_texts = {
            'title': 'Enter a title of your recipe.',
            'description': 'Describe how to prepare a dish.',
            'image': 'Upload an image of prepared dish.',
        }


class RecipeIngredientForm(forms.Form):
    """
    The form that is used to add associate an ingredient with a given recipe.
    Note that several of these forms must be used in order to add more than one
    ingredient. For this, JavaScript can be employed to create them on the fly.
    Also note that no recipe is chosen: this is done so because recipe is not
    yet created, as the form is shown on the same page. Probably could be done
    with AJAX, but too much trouble - this way is simpler (at the moment).
    """

    help_texts = {
        'ingredient': 'Select an ingredient that is needed for the recipe.',
        'unit': 'Select what unit should be used to measure the ingredient.',
        'quantity': 'Select quantity of the ingredient to be used.'
    }

    ingredient = forms.ModelChoiceField(queryset=Ingredient.objects.all(),
                                        help_text=help_texts['ingredient'])
    unit = forms.ModelChoiceField(queryset=Unit.objects.all(),
                                  help_text=help_texts['unit'])
    quantity = forms.FloatField(min_value=0, help_text=help_texts['quantity'])


class BaseRecipeIngredientFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
        """
        Avoids the problem where the user may try to add a recipe & a formset
        without entering any value in ingredient form. If init is not
        overriden, then entering nothing does not catch errors.
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


# Will need a second form for RecipeIngredient
# So use formsets
# http://stackoverflow.com/questions/28054991/combining-two-forms-in-one-django-view
# https://docs.djangoproject.com/en/1.10/topics/forms/formsets/
# Also, needs to add additional form for every ingredient. Calls for JS:
# http://stackoverflow.com/questions/5478432/making-a-django-form-class-with-a-dynamic-number-of-fields
# (second answer seems to be about right).
