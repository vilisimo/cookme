from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect

from fridge.models import Fridge
from .models import Recipe, RecipeIngredient

RECIPES_PER_PAGE = 12


def recipes(request):
    """
    Shows the list of recipes.

    :param request: standard request object.
    :return: standard HttpResponse object.
    """

    all_recipes = Recipe.objects.all().order_by('date')
    paginator = Paginator(all_recipes, RECIPES_PER_PAGE)
    page = request.GET.get('page')

    try:
        recipe_list = paginator.page(page)
    except PageNotAnInteger:
        recipe_list = paginator.page(1)
    except EmptyPage:
        recipe_list = paginator.page(paginator.num_pages)

    context = {
        'recipes': recipe_list,
        'user': request.user,
    }

    user = request.user
    if user.is_authenticated:
        fridge = Fridge.objects.get_or_create(user=user)[0]
        user_recipes = fridge.recipes.all()
        context['user_recipes'] = user_recipes

    return render(request, 'recipes/recipes.html', context)


def recipe_detail(request, slug):
    """
    Displays details of a particular recipe.

    :param request: standard request object.
    :param slug: slug passed from urls for identification of recipe.
    :return: standard HttpResponse object.
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
        'user': request.user,
        'pk': recipe.pk,
    }

    user = request.user
    if user.is_authenticated:
        fridge = Fridge.objects.get_or_create(user=user)[0]
        user_recipes = fridge.recipes.all().values_list('id', flat=True)
        context['user_recipes'] = user_recipes

    return render(request, 'recipes/recipe_detail.html', context)


@login_required
def add_to_fridge(request, pk):
    """
    Adds recipes to user's fridge.

    :param request: standard request object.
    :param pk: recipe's primary key.
    :return: standard HttpResponse object.
    """

    user = request.user
    fridge = Fridge.objects.get_or_create(user=user)[0]
    recipe = Recipe.objects.get(pk=pk)
    # In case user tried to add the same recipe twice
    if recipe not in fridge.recipes.all():
        fridge.recipes.add(recipe)
    url = reverse('fridge:fridge_detail')

    return HttpResponseRedirect(url)
