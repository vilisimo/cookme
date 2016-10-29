"""
Logic related to searching fridge & global recipes lives.
"""

from django.shortcuts import render
from django.db.models import Q

from recipes.models import Recipe
from .helpers import decode, get_name_set


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

        # # In case testing reveals something fishy:
        # recipes = Recipe.objects.all()
        # for recipe in recipes:
        #     recipe_ings = set([ing.name for ing in recipe.ingredients.all()])
        #     if ingredients.issubset(recipe_ings):
        #         matched.append(recipe)
        matched = Recipe.objects.exclude(~Q(ingredients__name__in=ingredients))

    content = {
        'ingredients': ingredients,
        'recipes': matched,
    }

    return render(request, 'search/search_results.html', content)
