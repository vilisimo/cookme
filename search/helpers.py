"""
Helper functions to support functionality related to searching the recipes.
"""


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
