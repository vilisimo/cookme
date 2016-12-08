from django.shortcuts import render, get_object_or_404

from .models import Ingredient
from recipes.models import Recipe


def ingredient_detail(request, slug):
    """
    View responsible for showing detailed ingredient info.

    :param request: standard request object.
    :param slug: slug of a desired ingredient.
    :return: standard HttpResponse object.
    """

    ingredient = get_object_or_404(Ingredient, slug=slug)
    recipes = Recipe.objects.filter(ingredients__name__exact=ingredient.name)

    content = {
        'ingredient': ingredient,
        'recipes': recipes,
    }

    return render(request, 'ingredients/ingredient_detail.html', content)
