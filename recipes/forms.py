from string import capwords

from django.conf import settings
from django.core.files.images import get_image_dimensions
from django.forms import (
    TextInput,
    NumberInput,
    Textarea,
    Select,
    ModelForm,
    BaseFormSet,
    ModelChoiceField,
    ValidationError,
    CharField
)
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

from ingredients.models import Ingredient, Unit
from .models import DEFAULT_IMAGE_LOCATION
from .models import RecipeIngredient, Recipe


class AddRecipeForm(ModelForm):
    """
    Recipe instance form. Creates a recipe and adds it to a fridge.

    Note: If user wants to add an exiting recipe to a fridge, he/she has to
    navigate to that recipe and click an appropriate button.
    """

    def __init__(self, *args, **kwargs):
        super(AddRecipeForm, self).__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({
            'data-width': settings.MAX_WIDTH,
            'data-height': settings.MAX_HEIGHT
        })

    # Validates that image is of appropriate dimensions
    def clean_image(self):
        image = self.cleaned_data.get('image')

        if image and image != DEFAULT_IMAGE_LOCATION:
            width, height = get_image_dimensions(image)
            if width > settings.MAX_WIDTH or height > settings.MAX_HEIGHT:
                error = f"Uploaded image is too big. <br/>Allowed dimensions: " \
                        f"{settings.MAX_WIDTH} x {settings.MAX_HEIGHT}.<br/>" \
                        f"Uploaded image: {width} x {height}"
                raise ValidationError(mark_safe(error))
            return image

    class Meta:
        model = Recipe
        fields = ('title', 'description', 'steps', 'cuisine', 'image',)

        widgets = {
            'title': TextInput(
                attrs={'placeholder': 'Recipe\'s title'}
            ),
            'description': Textarea(
                attrs={'placeholder': 'Please provide a short description of '
                                      'the recipe.'}
            ),
            'steps': Textarea(
                attrs={'placeholder': 'Please explain how to prepare a dish. '
                                      'Provide each step on a new line. '
                                      'Multiple new lines can be used.'}
            ),
            'cuisine': Select(
                attrs={'required': 'true'}
            )
        }

        labels = {
            'title': '',
            'description': '',
            'steps': '',
        }


class RecipeIngredientForm(ModelForm):
    """
    Associates an ingredient with a given recipe. That is, this form supplements
    the above one and should be used in conjunction with it. Workflow:
        - fill in recipe's details
        - add ingredients to the recipe
        - submit
        -> recipe created, ingredients created/found and associated with recipe.

    Note that several of these forms must be used in order to add more than one
    ingredient. For this, JavaScript can be employed to create them on the fly.

    Also note that recipe is excluded: this is done so because recipe is not
    yet created, as the form is shown on the same page.

    Note that even though HTML5 validation for minimum numbers is employed,
    there is also a MinValueValidator in the RecipeIngredient model, to ensure
    that there is no situation where < 0 value is provided.
    """

    unit = ModelChoiceField(queryset=Unit.objects.all(), empty_label=None)
    ingredientFieldAttributes = {
        'required': 'true',
        'placeholder': 'Enter ingredient'
    }
    ingredient = CharField(widget=TextInput(attrs=ingredientFieldAttributes))

    class Meta:
        model = RecipeIngredient
        exclude = ('recipe', 'ingredient')

        widgets = {
            'unit': Select(attrs={'required': 'true'}),
            'quantity': NumberInput(attrs={'required': 'true', 'min': '0',
                                    'placeholder': 'Enter quantity'}),
        }

    def save(self, commit=True):
        """
        Allows the user to enter an ingredient instead of selecting it.

        Unfortunately, copy-paste from fridge/forms, since ModelForm
        inheritance is slightly tricky and IA need more time to figure it out
        properly.
        """

        # Take the input string, create ingredient that has the same name.
        ingredient_name = capwords(self.cleaned_data['ingredient'])
        ing = Ingredient.objects.get_or_create(name=ingredient_name)[0]
        self.instance.ingredient = ing

        return super(RecipeIngredientForm, self).save(commit)


class BaseRecipeIngredientFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
        """
        Avoids the problem where the user may try to add a recipe & a formset
        without entering any value in ingredient form. If init is not
        overridden, then entering nothing does not catch errors.
        """

        super(BaseRecipeIngredientFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False

    def clean(self):
        """ Ensure that the same two ingredients cannot be chosen """

        if any(self.errors):
            return

        if not self.forms[0].has_changed():
            raise ValidationError(_('Please add at least one field.'))

        ingredients = []
        for form in self.forms:
            ingredient = form.cleaned_data['ingredient']
            if ingredient in ingredients:
                raise ValidationError(_('Ingredients should be distinct.'))
            ingredients.append(ingredient)
