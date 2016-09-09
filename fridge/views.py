from django.shortcuts import render, get_object_or_404

from django.contrib.auth.decorators import login_required

from .models import Fridge
from .models import FridgeIngredient


@login_required
def fridge_detail(request):
    """
    View responsible for displaying the user's fridge.

    :param  request: default request object
    :return:         default render object
    """

    user = request.user
    # If no fridge is found, should redirect to creation of fridge. Or, ideally,
    # upon registration a fridge should be created.
    fridge = get_object_or_404(Fridge, user=user)
    ingredients = FridgeIngredient.objects.filter(fridge=fridge)
    recipes = fridge.recipes.all()

    content = {
        'fridge': fridge,
        'ingredients': ingredients,
        'recipes': recipes,
    }

    return render(request, 'fridge/fridge_detail.html', content)
