"""
Functionality related to creating mock databases for testing.

However, keep in mind that some tests may require specific conditions,
thus it would be unwise for them to use general methods. They may change in
the future.
"""

from django.contrib.auth.models import User
from django.test import Client

from ingredients.models import Unit, Ingredient
from recipes.models import Recipe, RecipeIngredient as RecIng
from fridge.models import Fridge, FridgeIngredient as FI


def populate_ingredients():
    """
    Populates DB with a batch of ingredients.

    :return: a list of ingredients created.
    """

    i1 = Ingredient.objects.create(name='Meat', type='Meat')
    i2 = Ingredient.objects.create(name='Lemon', type='Fruit')
    i3 = Ingredient.objects.create(name='Apple', type='Fruit')
    i4 = Ingredient.objects.create(name='White Bread', type='Bread')

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

    user = User.objects.get_or_create(username='test', password='test')[0]
    fridge = Fridge.objects.get_or_create(user=user)[0]
    ingredients = populate_ingredients()
    units = populate_units()

    fi1 = FI.objects.create(fridge=fridge, ingredient=ingredients[0],
                            unit=units[0], quantity=1)
    fi2 = FI.objects.create(fridge=fridge, ingredient=ingredients[1],
                            unit=units[0], quantity=1)
    fi3 = FI.objects.create(fridge=fridge, ingredient=ingredients[2],
                            unit=units[0], quantity=1)
    fi4 = FI.objects.create(fridge=fridge, ingredient=ingredients[3],
                            unit=units[0], quantity=1)

    return [fi1, fi2, fi3, fi4]


def populate_recipes():
    """
    Creates a batch of test recipes with ingredients and all other necessary
    information to test most of the functionality.

    :return: a list of recipes created.
    """

    user = User.objects.get_or_create(username='test', password='test')[0]

    # Ingredients
    i1, i2, i3, i4 = populate_ingredients()
    # Units
    u = populate_units()[0]

    # Recipes
    r0 = Recipe.objects.create(author=user, title='MeatRec')
    RecIng.objects.create(recipe=r0, ingredient=i1, unit=u, quantity=1)

    r1 = Recipe.objects.create(author=user, title='MeatLemonAppleRec')
    RecIng.objects.create(recipe=r1, ingredient=i1, unit=u, quantity=1)
    RecIng.objects.create(recipe=r1, ingredient=i2, unit=u, quantity=1)
    RecIng.objects.create(recipe=r1, ingredient=i3, unit=u, quantity=1)

    r2 = Recipe.objects.create(author=user, title="AllIngredientsRec")
    RecIng.objects.create(recipe=r2, ingredient=i1, unit=u, quantity=1)
    RecIng.objects.create(recipe=r2, ingredient=i2, unit=u, quantity=1)
    RecIng.objects.create(recipe=r2, ingredient=i3, unit=u, quantity=1)
    RecIng.objects.create(recipe=r2, ingredient=i4, unit=u, quantity=1)

    r3 = Recipe.objects.create(author=user, title="LemonRec")
    RecIng.objects.create(recipe=r3, ingredient=i2, unit=u, quantity=1)

    return [r0, r1, r2, r3]


def logged_in_client(user=None):
    """ Creates logged in user. """

    client = Client()
    if user:
        client.login(username=user.username, password=user.password)
    else:
        client.login(username='test', password='test')
    return client
