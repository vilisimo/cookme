"""
Logic related to searching fridge & global recipes lives.
"""

from django.shortcuts import render

from recipes.models import Recipe
from .helpers import decode, get_name_set


def search_results(request):
    """
    Shows the results of a search from a main page.

    :param request: default request object.
    :return: default render object.
    """

    ingredients = request.GET.get('q')
    matched = []
    if ingredients:
        ingredients = decode(ingredients)
        ingredients = get_name_set(ingredients)

        recipes = Recipe.objects.all()
        for recipe in recipes:
            recipe_ings = set([ing.name for ing in recipe.ingredients.all()])
            if ingredients.issubset(recipe_ings):
                matched.append(recipe)

    content = {
        'ingredients': ingredients,
        'recipes': matched,
    }

    return render(request, 'search/search_results.html', content)
