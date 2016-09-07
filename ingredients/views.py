from django.shortcuts import render, get_object_or_404

from .models import Ingredient


def ingredient_detail(request, slug):
    """
    View responsible for showing detailed ingredient info.

    :param request: standard request object
    :param pk: primary key of an ingredient
    :return: standard render object
    """

    ingredient = get_object_or_404(Ingredient, slug=slug)

    content = {
        'ingredient': ingredient,
    }

    return render(request, 'ingredients/ingredient_detail.html', content)
