from django.shortcuts import render, get_object_or_404

from django.contrib.auth.decorators import login_required

from .models import Fridge
from .models import FridgeIngredient


@login_required
def add_recipe(request):
    """
    View that is responsible for displaying a form to add a recipe to user's
    fridge. Note that recipe is added both to the user's fridge and the
    global recipe list.

    :param request: default request object
    :return:        default render object
    """

    # We always want to ensure that a user has a fridge to add recipes to.
    Fridge.objects.get_or_create(user=request.user)

    content = {
        'user': request.user,
    }

    return render(request, 'fridge/add_recipe.html', content)


@login_required
def fridge_detail(request):
    """
    View responsible for displaying the user's fridge.

    :param  request: default request object
    :return:         default render object
    """

    user = request.user
    fridge = get_object_or_404(Fridge, user=user)
    ingredients = FridgeIngredient.objects.filter(fridge=fridge)
    recipes = fridge.recipes.all()

    content = {
        'fridge': fridge,
        'ingredients': ingredients,
        'recipes': recipes,
    }

    return render(request, 'fridge/fridge_detail.html', content)


