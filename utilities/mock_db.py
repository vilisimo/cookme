"""
Functionality related to creating mock databases for testing.

However, keep in mind that some tests may require specific conditions,
thus it would be unwise for them to use general methods. They may change in
the future.
"""

from django.test import Client

from fridge.models import Fridge, FridgeIngredient as FI
from ingredients.models import Unit, Ingredient
from recipes.models import Recipe, RecipeIngredient as RI
from .populate import get_user


def populate_ingredients():
    """
    Populates DB with a batch of ingredients.

    :return: a list of ingredients created.
    """

    Ingredient.objects.get_or_create(name='Meat', type='Meat')
    Ingredient.objects.get_or_create(name='Lemon', type='Fruit')
    Ingredient.objects.get_or_create(name='Apple', type='Fruit')
    Ingredient.objects.get_or_create(name='White Bread', type='Bread')
    ingredients = Ingredient.objects.all()

    return ingredients


def populate_units(name='kilogram', abbrev='kg'):
    """
    Populates mock DB with unit entities.

    :return: a (list of) unit(s) created.
    """

    Unit.objects.get_or_create(name=name, abbrev=abbrev)
    # In case more than one unit is ever created.
    units = Unit.objects.all()

    return units


def populate_fridge_ingredients():
    """
    Populates mock DB with fridge ingredient entities.

    :return: a list of fridge ingredients created.
    """

    user = get_user(username='test', password='test')
    fridge = Fridge.objects.get_or_create(user=user)[0]
    ingredients = populate_ingredients()
    units = populate_units()

    FI.objects.get_or_create(fridge=fridge, ingredient=ingredients[0], unit=units[0], quantity=1)
    FI.objects.get_or_create(fridge=fridge, ingredient=ingredients[1], unit=units[0], quantity=1)
    FI.objects.get_or_create(fridge=fridge, ingredient=ingredients[2], unit=units[0], quantity=1)
    FI.objects.get_or_create(fridge=fridge, ingredient=ingredients[3], unit=units[0], quantity=1)
    fridge_ingredients = FI.objects.all()

    return fridge_ingredients


def populate_fridge_recipes():
    """
    Creates a batch of recipes that are associated with a fridge of test user.

    :return: a list of recipes created.
    """

    user = get_user(username='test', password='test')
    fridge = Fridge.objects.get_or_create(user=user)[0]
    recipes = populate_recipes()
    fridge.recipes.add(*recipes)
    fridge_recipes = fridge.recipes.all()
    return fridge_recipes


def populate_recipes():
    """
    Creates a batch of test recipes with ingredients and all other necessary
    information to test most of the functionality.

    :return: a QuerySet of recipes created.
    """

    user = get_user(username='test', password='test')

    # Ingredients. Can be done in one line, but this way avoids problems if
    # more than 4 ingredients are returned.
    ingredients = populate_ingredients()
    i1 = ingredients[0]
    i2 = ingredients[1]
    i3 = ingredients[2]
    i4 = ingredients[3]

    # Units
    u = populate_units()[0]

    # Recipes
    r0 = Recipe.objects.get_or_create(author=user, title='Meatrec')[0]
    RI.objects.get_or_create(recipe=r0, ingredient=i1, unit=u, quantity=1)

    r1 = Recipe.objects.get_or_create(author=user, title='Meatlemonapplerec')[0]
    RI.objects.get_or_create(recipe=r1, ingredient=i1, unit=u, quantity=1)
    RI.objects.get_or_create(recipe=r1, ingredient=i2, unit=u, quantity=1)
    RI.objects.get_or_create(recipe=r1, ingredient=i3, unit=u, quantity=1)

    r2 = Recipe.objects.get_or_create(author=user, title="Allingredientsrec")[0]
    RI.objects.get_or_create(recipe=r2, ingredient=i1, unit=u, quantity=1)
    RI.objects.get_or_create(recipe=r2, ingredient=i2, unit=u, quantity=1)
    RI.objects.get_or_create(recipe=r2, ingredient=i3, unit=u, quantity=1)
    RI.objects.get_or_create(recipe=r2, ingredient=i4, unit=u, quantity=1)

    r3 = Recipe.objects.get_or_create(author=user, title="Lemonrec")[0]
    RI.objects.get_or_create(recipe=r3, ingredient=i2, unit=u, quantity=1)

    recipes = Recipe.objects.all()

    return recipes


def logged_in_client(user=None):
    """ Creates logged in user. """

    client = Client()
    if user:
        client.login(username=user.username, password=user.password)
    else:
        client.login(username='test', password='test')
    return client
