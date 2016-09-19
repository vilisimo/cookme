from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.forms import formset_factory

from .forms import AddRecipeFridgeForm
from recipes.forms import BaseRecipeIngredientFormSet, RecipeIngredientForm
from .models import FridgeIngredient, Fridge


@login_required
def add_recipe(request):
    """
    Responsible for displaying a form to add a recipe to user's fridge.

    Note that recipe is added both to the user's fridge and the global recipe
    list. This is so because the recipe is created from a fridge's view, hence
    it is logical that a fridge should be updated with it.

    Also note that a recipe might have several ingredients. Thus, it is
    necessary to have formset for RecipeIngredientForm. Also, it is necessary
    to have some JavaScript that would add more forms to a formset if the
    user requires more than one ingredient (very likely).


    :param request: default request object
    :return:        default render object (GET); redirect to fridge (POST)
    """

    # Ensure that a user has a fridge to add recipes to, even if non-existent
    # before requesting to add a recipe (should be impossible, but who knows).
    user = request.user
    fridge, created = Fridge.objects.get_or_create(user=user)
    RecInFormset = formset_factory(RecipeIngredientForm,
                                   formset=BaseRecipeIngredientFormSet)

    if request.method == 'POST':
        form = AddRecipeFridgeForm(request.POST, request.FILES)
        formset = RecInFormset(request.POST)
        if all([form.is_valid(), formset.is_valid()]):
            # Author field cannot be null. Hence, assign authorship to the user.
            recipe = form.save(commit=False)
            recipe.author = user
            recipe.save()
            fridge.recipes.add(recipe)

            for f in formset:
                # Ingredients need recipe FK.
                ingredient = f.save(commit=False)
                ingredient.recipe = recipe
                ingredient.save()

            url = reverse('fridge:fridge_detail')

            return HttpResponseRedirect(url)

    else:
        form = AddRecipeFridgeForm()
        formset = RecInFormset()

    content = {
        'user': user,   # No need to send if decide to set user in this view
        'form': form,
        'formset': formset,
    }

    return render(request, 'fridge/add_recipe.html', content)


@login_required
def fridge_detail(request):
    """
    Responsible for displaying the user's fridge.

    :param  request: default request object
    :return:         default render object
    """

    user = request.user
    fridge, created = Fridge.objects.get_or_create(user=user)
    ingredients = FridgeIngredient.objects.filter(fridge=fridge)
    recipes = fridge.recipes.all()

    content = {
        'fridge': fridge,
        'ingredients': ingredients,
        'recipes': recipes,
    }

    return render(request, 'fridge/fridge_detail.html', content)


