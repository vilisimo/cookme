"""
Logic related to searching fridge & global recipes lives.
"""

from django.db.models import Q
from django.shortcuts import render

from recipes.models import Recipe
from ingredients.models import Ingredient
from utilities.search_helpers import decode, get_name_set, match_recipes


def search_results(request):
    """
    Shows a list of recipes that have the ingredients entered.

    Note: ingredients entered are a subset of a recipe, not a superset.

    :param request: default request object.
    :return: default render object.
    """

    ingredients = request.GET.get('q')
    matched = []
    if ingredients:
        ingredients = decode(ingredients)
        ingredients = get_name_set(ingredients)
        matched = match_recipes(ingredients)

    content = {
        'ingredients': ingredients,
        'recipes': matched,
    }

    return render(request, 'search/search_results.html', content)
