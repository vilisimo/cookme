from django.forms import ModelForm

from .models import Recipe


class AddRecipeFridgeForm(ModelForm):
    """
    The form to create a recipe instance. That is, create a recipe and add it
    to a fridge. If user wants to add an exiting recipe to a fridge, he/she
    has to navigate to that fridge and click appropriate button.
    """

    class Meta:
        model = Recipe
        fields = ("title", "description", "image", )


# Will need a second form for RecipeIngredient
# So use formsets
# http://stackoverflow.com/questions/28054991/combining-two-forms-in-one-django-view
# https://docs.djangoproject.com/en/1.10/topics/forms/formsets/
# Also, needs to add additional form for every ingredient. Calls for JS:
# http://stackoverflow.com/questions/5478432/making-a-django-form-class-with-a-dynamic-number-of-fields
# (second answer seems to be about right).
