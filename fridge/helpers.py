from string import capwords

from recipes.models import Recipe
from ingredients.models import Ingredient


def get_fridge_recipes(ingredients):
    """
    Returns a list of recipes that contain ingredients from a list and
    nothing more (but they do not have to have every ingredient).

    Logic: first of all, get all ingredients that are not found in a set.
    This is a list of ingredients that we do not want recipes to contain.
    Once we have this list, we can select only those recipes that do not
    contain any of these ingredients, leaving us with a query set of recipes
    that actually contain only those ingredients that we are interested in.

    :param ingredients: a set of CAPITALIZED ingredients of which at least one
                        should be in a recipe.
    :return: QuerySet of recipe objects that have at least one ingredient.
    """

    # Ensures set contents are capitalized, as DB expects capitalized names.
    # Should never need to capitalize ingredients, but just in case it happens.
    ingredients = [ingredient if ingredient.istitle() else
                   capwords(ingredient) for ingredient in ingredients]

    # Get all the ingredients that do not match our set.
    non_matching = Ingredient.objects.exclude(name__in=ingredients)

    # Now get all recipes that do not have these ingredients.
    recipes = Recipe.objects.exclude(ingredients__in=non_matching)

    return recipes
