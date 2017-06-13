from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.forms import formset_factory
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect

from recipes.forms import (
    BaseRecipeIngredientFormSet,
    RecipeIngredientForm,
    AddRecipeForm,
)
from recipes.models import Recipe
from utilities.search_helpers import subset_recipes
from .forms import FridgeIngredientForm
from .models import FridgeIngredient, Fridge


@login_required
def add_recipe(request):
    """
    Responsible for displaying a form to add a recipe to a user's fridge.

    Note that recipe is added both to the user's fridge and the global recipe
    list. This is so because the recipe is created from a fridge's view, hence
    it is logical that a fridge should be updated with it.

    Also note that a recipe might have several ingredients. Thus, it is
    necessary to have formset for RecipeIngredientForm. Also, it is necessary
    to have some JavaScript that would add more forms to a formset if the
    user requires more than one ingredient (very likely).


    :param request: default request object.
    :return: default HttpResponse object (GET); redirect to fridge (POST).
    """

    # Ensure that a user has a fridge to add recipes to, even if non-existent
    # before requesting to add a recipe (should be impossible, but who knows).
    user = request.user
    fridge = Fridge.objects.get_or_create(user=user)[0]
    RecInFormset = formset_factory(RecipeIngredientForm,
                                   formset=BaseRecipeIngredientFormSet)

    if request.method == 'POST':
        form = AddRecipeForm(request.POST, request.FILES)
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
        form = AddRecipeForm()
        formset = RecInFormset()

    content = {
        'user': user,   # Not really used anywhere, could probably delete it.
        'form': form,
        'formset': formset,
    }

    return render(request, 'fridge/add_recipe.html', content)


@login_required
def fridge_detail(request):
    """
    Responsible for displaying user's fridge.

    Note that form to add an ingredient is also shown here, as there is no
    need for a separate page for such a small form.

    Form logic: if we try to add something that already exists, we do not
    want to create a separate FridgeIngredient instance. We want to update
    the existing one. The only thing that changes is quantity, thus we
    increment it. Alternatively, a new value could be used instead. On the
    other hand, if a FridgeIngredient instance does not exists, we create it,
    by passing in a fridge, which is not supplied with a form (but is required).

    NOTE: incrementing is not perfect at the moment. If user has 2 units of
    lemons, and adds another 500 grams of lemons, he/she will end up with 502
    units of lemons, which is stupid. JS/AJAX to fix it? Separate functions
    to convert it?

    :param request: default request object.
    :return: default HttpResponse object.
    """

    user = request.user
    fridge = Fridge.objects.get_or_create(user=user)[0]
    ingredients = FridgeIngredient.objects.filter(fridge=fridge)
    recipes = fridge.recipes.all()

    if request.method == 'POST':
        form = FridgeIngredientForm(request.POST)
        if form.is_valid():
            fi = form.save(commit=False)
            try:
                # If F.I. exists, we do not need to create it, only update it.
                fi = FridgeIngredient.objects.get(fridge=fridge,
                                                  ingredient=fi.ingredient)
                fi.quantity += float(form.cleaned_data['quantity'])
            except FridgeIngredient.DoesNotExist:
                # If it does not, we need to supply fridge in order to save it.
                fi.fridge = fridge
            fi.save()

            url = reverse('fridge:fridge_detail')

            return HttpResponseRedirect(url)
    else:
        form = FridgeIngredientForm()

    content = {
        'fridge': fridge,
        'ingredients': ingredients,
        'recipes': recipes,
        'form': form,
    }

    return render(request, 'fridge/fridge_detail.html', content)


@login_required
def remove_ingredient(request, pk):
    """
    View used to remove an ingredient from a fridge.

    Note that in case the user is not the same as the one that owns the
    fridge with a given FridgeIngredient, he/she is redirected to home page.

    Note: good place to use AJAX to avoid refreshing the page?

    :param request: standard request object.
    :param pk: primary key of the ingredient to be deleted.
    """

    url = reverse('fridge:fridge_detail')
    ingredient = get_object_or_404(FridgeIngredient, pk=pk)
    if request.user != ingredient.fridge.user:
        return HttpResponseRedirect(reverse('home'))
    ingredient.delete()

    return HttpResponseRedirect(url)


@login_required
def remove_recipe(request, pk):
    """
    View that is responsible for removing recipes from user's fridge. Note
    that recipes are not removed from 'global' recipe list.

    Note: good place to use AJAX to avoid refreshing the page?

    :param request: standard request object.
    :param pk: to-be-removed recipe's primary key.
    :return: HttpResponse object.
    """

    url = reverse('fridge:fridge_detail')
    recipe = get_object_or_404(Recipe, pk=pk)
    fridge = request.user.fridge
    fridge.recipes.remove(recipe)

    return HttpResponseRedirect(url)


@login_required
def possibilities(request):
    """
    Shows recipes that can be made with the ingredients in a fridge.

    NOTE: ingredients are matched against ALL recipes, not only those in a
    fridge.

    :param request: standard request object.
    :return: standard HttpResponse object.
    """

    user = request.user
    fridge = Fridge.objects.get_or_create(user=user)[0]
    ingredients = fridge.ingredients.all()
    ingredients = [ingredient.name for ingredient in ingredients]

    recipes = subset_recipes(ingredients)

    content = {
        'ingredients': ingredients,
        'recipes': recipes,
    }

    return render(request, 'fridge/possibilities.html', content)


@login_required
def fridge_recipes(request):
    """
    Chooses recipes from those in the fridge that can be made with ingredients
    that are in the fridge.

    NOTE: very similar to above one. CBVs may be able to fix it?

    :param request: standard request object.
    :return: standard HttpResponse object.
    """

    user = request.user
    fridge = Fridge.objects.get_or_create(user=user)[0]
    fridge_ingredients = fridge.ingredients.all()
    ingredient_names = [ingredient.name for ingredient in fridge_ingredients]
    recipes = subset_recipes(ingredient_names, fridge=fridge)

    content = {
        'ingredients': ingredient_names,
        'recipes': recipes,
    }

    return render(request, 'fridge/fridge_recipes.html', content)
