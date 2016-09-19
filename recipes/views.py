from django.shortcuts import render, get_object_or_404

from .models import Recipe, RecipeIngredient


def recipes(request):
    """
    Should show the list of recipes.

    :param request: standard request object.
    :return:        standard render object.
    """

    recipe_list = Recipe.objects.all()
    context = {
        'recipes': recipe_list
    }

    return render(request, 'recipes/recipes.html', context)


def recipe_detail(request, slug):
    """
    View responsible for displaying a particular recipe.

    :param request: standard request object.
    :param slug:    slug passed from urls for identification of recipe.
    :return:        standard render object.
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
    }

    return render(request, 'recipes/recipe_detail.html', context)
