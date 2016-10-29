"""
Helper functions to support functionality related to searching the recipes.
"""

from string import capwords

from recipes.models import Recipe
from ingredients.models import Ingredient


def encode(query):
    """
    Takes care of proper formatting of the query strings.

    User may enter ingredients/recipes that have more than one word, hence there
    has to be some way to distinguish multi-word ingredients from single-word
    ones. Hence, every new term must be separated by a comma, and spaces have to
    be encoded as '-' (or anything else, really). Otherwise, they would be
    picked up as a separate ingredients/recipes/etc.

    Example:
        query:      lemongrass, lemon, lime juice
        formatted:  lemongrass lemon lime-juice
    This string can be further encoded and passed to a search view.

    :param query: query that has to be transformed into a proper query string.
    :return: string. Formatted according to the above considerations.
    """

    separate_terms = query.split(',')
    dash_separated = [term.strip().replace(' ', '-') for term in separate_terms]
    formatted = " ".join(dash_separated)

    return formatted


def decode(query):
    """
    Removes dashes from a given query, and adds commas after each term, so that
    the string is returned to the same form the user has entered. Forgetting
    to add commas would create the similar problem as above: how to distinguish
    terms from one another.

    Note: user may leave a blank space after a comma. It is removed here so
    that the processing later is more straightforward.

    FUTURE NOTE: dashes may not be completely safe option. It is reasonable to
    expect that some ingredients/recipes may have dashes in their titles.
    However, for a practice project it is not of immediate importance.
    """

    split = query.split()
    decoded = ",".join(term.replace('-', ' ') for term in split)

    return decoded


def get_name_set(decoded_query):
    """
    Extracts a set of ingredient names from decoded query, capitalizes them,
    puts them in a set so that it is ready to use.

    :param decoded_query: query that was passed by a search and decoded.
    :return: a set of ingredient names (capitalized for easier use).
    """

    names = set([capwords(name) for name in decoded_query.split(',')])
    return names


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
