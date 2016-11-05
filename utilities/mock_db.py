"""
Functionality related to creating mock databases for testing.

However, keep in mind that some tests may require specific conditions,
thus it would be unwise for them to use general methods. They may change in
the future.
"""

from django.test import Client

from ingredients.models import Unit, Ingredient
from recipes.models import Recipe, RecipeIngredient as RI
from fridge.models import Fridge, FridgeIngredient as FI

from .populate import get_user


def populate_ingredients():
    """
    Populates DB with a batch of ingredients.

    :return: a list of ingredients created.
    """

    i1 = Ingredient.objects.get_or_create(name='Meat', type='Meat')[0]
    i2 = Ingredient.objects.get_or_create(name='Lemon', type='Fruit')[0]
    i3 = Ingredient.objects.get_or_create(name='Apple', type='Fruit')[0]
    i4 = Ingredient.objects.get_or_create(name='White Bread', type='Bread')[0]

    return [i1, i2, i3, i4]


def populate_units(name='kilogram', abbrev='kg'):
    """
    Populates mock DB with unit entities.

    :return: a (list of) unit(s) created.
    """

    u1 = Unit.objects.get_or_create(name=name, abbrev=abbrev)[0]

    return [u1]


def populate_fridge_ingredients():
    """
    Populates mock DB with fridge ingredient entities.

    :return: a list of fridge ingredients created.
    """

    user = get_user(username='test', password='test')
    fridge = Fridge.objects.get_or_create(user=user)[0]
    ingredients = populate_ingredients()
    units = populate_units()

    fi1 = FI.objects.get_or_create(fridge=fridge, ingredient=ingredients[0],
                                   unit=units[0], quantity=1)[0]
    fi2 = FI.objects.get_or_create(fridge=fridge, ingredient=ingredients[1],
                                   unit=units[0], quantity=1)[0]
    fi3 = FI.objects.get_or_create(fridge=fridge, ingredient=ingredients[2],
                                   unit=units[0], quantity=1)[0]
    fi4 = FI.objects.get_or_create(fridge=fridge, ingredient=ingredients[3],
                                   unit=units[0], quantity=1)[0]

    return [fi1, fi2, fi3, fi4]


def populate_recipes():
    """
    Creates a batch of test recipes with ingredients and all other necessary
    information to test most of the functionality.

    :return: a list of recipes created.
    """

    user = get_user(username='test', password='test')

    # Ingredients
    i1, i2, i3, i4 = populate_ingredients()
    # Units
    u = populate_units()[0]

    # Recipes
    r0 = Recipe.objects.get_or_create(author=user, title='MeatRec')[0]
    RI.objects.create(recipe=r0, ingredient=i1, unit=u, quantity=1)

    r1 = Recipe.objects.get_or_create(author=user, title='MeatLemonAppleRec')[0]
    RI.objects.get_or_create(recipe=r1, ingredient=i1, unit=u, quantity=1)
    RI.objects.get_or_create(recipe=r1, ingredient=i2, unit=u, quantity=1)
    RI.objects.get_or_create(recipe=r1, ingredient=i3, unit=u, quantity=1)

    r2 = Recipe.objects.get_or_create(author=user, title="AllIngredientsRec")[0]
    RI.objects.create(recipe=r2, ingredient=i1, unit=u, quantity=1)
    RI.objects.create(recipe=r2, ingredient=i2, unit=u, quantity=1)
    RI.objects.create(recipe=r2, ingredient=i3, unit=u, quantity=1)
    RI.objects.create(recipe=r2, ingredient=i4, unit=u, quantity=1)

    r3 = Recipe.objects.get_or_create(author=user, title="LemonRec")[0]
    RI.objects.create(recipe=r3, ingredient=i2, unit=u, quantity=1)

    return [r0, r1, r2, r3]


def logged_in_client(user=None):
    """ Creates logged in user. """

    client = Client()
    if user:
        client.login(username=user.username, password=user.password)
    else:
        client.login(username='test', password='test')
    return client
