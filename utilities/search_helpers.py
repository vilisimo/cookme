"""
Helper functions to support functionality related to searching the recipes.
"""

from string import capwords

from django.db.models import Count

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


def match_recipes(ingredients):
    """
    Matches given ingredients against recipes to see which recipes contain
    given ingredients (and possibly more).

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

