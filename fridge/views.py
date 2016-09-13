from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from .models import Fridge
from .models import FridgeIngredient
from .forms import AddRecipeFridgeForm


@login_required
def add_recipe(request):
    """
    View that is responsible for displaying a form to add a recipe to user's
    fridge. Note that recipe is added both to the user's fridge and the
    global recipe list.

    :param request: default request object
    :return:        default render object
    """

    # Ensure that a user has a fridge to add recipes to, even if non-existent
    # before requesting to add a recipe (should be impossible, but who knows).
    user = request.user
    fridge, created = Fridge.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = AddRecipeFridgeForm(request.POST)
        if form.is_valid():
            # Form only has title, description and image. However, author field
            # cannot be null. Hence, assign authorship to the user.
            recipe = form.save(commit=False)
            recipe.author = user
            recipe.save()
            # Add a recipe that was just created to a fridge as well.
            fridge.recipes.add(recipe)

            url = reverse('fridge:fridge_detail')

            return HttpResponseRedirect(url)

    else:
        form = AddRecipeFridgeForm()

    content = {
        'user': user,   # No need to send if decide to set user in this view
        'form': form,
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
    fridge, created = Fridge.objects.get_or_create(user=user)
    ingredients = FridgeIngredient.objects.filter(fridge=fridge)
    recipes = fridge.recipes.all()

    content = {
        'fridge': fridge,
        'ingredients': ingredients,
        'recipes': recipes,
    }

    return render(request, 'fridge/fridge_detail.html', content)

# Few more views are needed for deleting the recipes / ingredients


