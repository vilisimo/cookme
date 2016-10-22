"""
Helper functions to support functionality related to searching the recipes.
"""


def generate_querystring(query):
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
