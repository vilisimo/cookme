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


def populate_recipes():
    """
    Creates a batch of test recipes with ingredients and all other necessary
    information to test most of the functionality.
    """

    user = User.objects.create_user(username='test', password='test')

    # Ingredients
    i1 = Ingredient.objects.create(name='Meat', type='Meat')
    i2 = Ingredient.objects.create(name='Lemon', type='Fruit')
    i3 = Ingredient.objects.create(name='Apple', type='Fruit')
    i4 = Ingredient.objects.create(name='White Bread', type='Bread')
    # Units
    u = Unit.objects.create(name='kilogram', abbrev='kg')

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


def logged_in_client():
    """ Creates logged in user. """

    client = Client()
    client.login(username='test', password='test')
    return client
