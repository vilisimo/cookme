"""
Helper functions to support functionality related to searching the recipes.
"""

from string import capwords

from django.db.models import Count

from ingredients.models import Ingredient
from recipes.models import Recipe


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
    decoded = ",".join(term.strip().replace('-', ' ') for term in split)

    return decoded


def get_name_set(decoded_query):
    """
    Extracts a set of ingredient names from decoded query, capitalizes them,
    puts them in a set so that it is ready to use.

    :param decoded_query: query that was passed by a search and decoded.
    :return: a set of ingredient names (capitalized for easier use).
    """

    names = set([capwords(name).strip() for name in decoded_query.split(',')])
    return names


def superset_recipes(ingredients):
    """
    Matches given ingredients against recipes to see which recipes contain
    given ingredients (and possibly more). That is, recipe's ingredient should
    be a SUPERSET of ingredients.

    :param ingredients: an set of encoded (see above) ingredient names
    :return: a list of recipes that have matching ingredients.
    """

    # recipes = Recipe.objects.filter(ingredients__name__in=ingredients).distinct()
    # Surely there should be a better way to do it. The one below?
    # matched = []
    # for recipe in recipes:
    #     recipe_ings = set([ing.name for ing in recipe.ingredients.all()])
    #     if ingredients.issubset(recipe_ings):
    #         matched.append(recipe)

    # Pretty hairy SQL query.
    matched = (Recipe.objects.filter(ingredients__name__in=ingredients)
               .annotate(num_ings=Count('ingredients__name'))
               .filter(num_ings=len(ingredients)))

    return matched


def subset_recipes(ingredients):
    """
    Returns a list of recipes that contain ingredients from a list and
    nothing more (but they do not have to have every ingredient). That is,
    ingredients in a fridge should be a SUPERSET of recipe's ingredients.

    Logic: first of all, get all ingredients that are not found in a set.
    This is a list of ingredients that we do not want recipes to contain.
    Once we have this list, we can select only those recipes that do not
    contain any of these ingredients, leaving us with a query set of recipes
    that actually contain only those ingredients that we are interested in.

    NOTE: This function looks at ALL recipes, not only those that are in a
    fridge.

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

    # Now get all recipes that do not have these non-matching ingredients.
    recipes = Recipe.objects.exclude(ingredients__in=non_matching)

    return recipes


def fridge_subset_recipes(ingredients, recipes):
    """
    Returns a list of recipes that contain ingredients form a list and nothing
    more. Ingredients in the fridge are a superset of ingredients in a recipe.

    Note: this and above are almost identical functions. Would be nice to merge
    them, but would also be nice to avoid doing several queries (which happens
    when passing all recipes, in possibilities() case).

    :param ingredients: a set of capitalized ingredients of which at least
                        one should be in a recipe.
    :param recipes:     QuerySet of recipes that should be matched against
                        ingredients.
    :return: QuerySet of recipe objects. All ingredients from a recipe should
             be in ingredient set.
    """

    ingredients = [ingredient if ingredient.istitle() else
                   capwords(ingredient) for ingredient in ingredients]

    # Get all the ingredients that do not match our set.
    non_matching = Ingredient.objects.exclude(name__in=ingredients)

    # Now get all recipes that do not have these non-matching ingredients.
    recipes = recipes.exclude(ingredients__in=non_matching)

    return recipes


