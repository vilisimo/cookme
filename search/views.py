"""
Logic related to searching fridge & global recipes lives.
"""

from django.shortcuts import render

from utilities.search_helpers import decode, get_name_set, superset_recipes


def search_results(request):
    """
    Shows a list of recipes that have the ingredients entered.

    Note: ingredients entered are a subset of a recipe, not a superset.

    :param request: default request object.
    :return: standard HttpResponse object.
    """

    ingredients = request.GET.get('q')
    matched = []
    if ingredients:
        ingredients = decode(ingredients)
        ingredients = get_name_set(ingredients)
        matched = superset_recipes(ingredients)

    content = {
        'ingredients': ingredients,
        'recipes': matched,
    }

    return render(request, 'search/search_results.html', content)
