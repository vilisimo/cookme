from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from fridge.models import Fridge
from .models import Recipe, RecipeIngredient


def recipes(request):
    """
    Shows the list of recipes.

    :param request: standard request object.
    :return: standard HttpResponse object.
    """

    recipe_list = Recipe.objects.all()
    context = {
        'recipes': recipe_list,
        'user': request.user,
    }

    return render(request, 'recipes/recipes.html', context)


def recipe_detail(request, slug):
    """
    Displays details of a particular recipe.

    :param request: standard request object.
    :param slug: slug passed from urls for identification of recipe.
    :return: standard HttpResponse object.
    """

    recipe = get_object_or_404(Recipe, slug=slug)
    ingredients = RecipeIngredient.objects.filter(recipe=recipe)
    recipe.views += 1
    recipe.save()

    context = {
        'author': recipe.author,
        'title': recipe.title,
        'cuisine': recipe.get_cuisine_display(),
        'description': recipe.description,
        'date': recipe.date,
        'views': recipe.views,
        'image': recipe.image,
        'steps': recipe.step_list(),
        'ingredients': ingredients,
        'user': request.user,
        'pk': recipe.pk,
    }

    return render(request, 'recipes/recipe_detail.html', context)


@login_required
def add_to_fridge(request, pk):
    """
    Adds recipes to user's fridge.

    :param request: standard request object.
    :param pk: recipe's primary key.
    :return: standard HttpResponse object.
    """

    user = request.user
    fridge = Fridge.objects.get_or_create(user=user)[0]
    recipe = Recipe.objects.get(pk=pk)
    # In case user tried to add the same recipe twice
    if recipe not in fridge.recipes.all():
        fridge.recipes.add(recipe)
    url = reverse('fridge:fridge_detail')

    return HttpResponseRedirect(url)
