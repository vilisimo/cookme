import os
import sys

project_path = os.path.normpath(os.getcwd() + os.sep + os.pardir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cookme.settings")
sys.path.append(project_path)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from recipes.models import Recipe
from ingredients.models import Ingredient, Unit


class bcolors:
    OKBLUE = '\033[94m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def populate_units(units_txt=None):
    """
    Populates or updates the database with units that are parsed from a txt
    file.
    """
    try:
        with open(units_txt) as f:
            f.readline()  # Get rid of the title line
            for line in f:
                line = [item.strip() for item in line.strip().split(';')]
                # Get or create is used in case we need to update the DB rather
                # than populate it from scratch.
                Unit.objects.get_or_create(name=line[0],
                                           abbrev=line[1],
                                           description=line[2])
        print(bcolors.OKBLUE + "Unit population is done." + bcolors.ENDC)
    except (FileNotFoundError, TypeError):
        print(bcolors.FAIL +
              "Input file was not recognized. Please check your input." +
              bcolors.ENDC)


def populate_ingredients(ingredients_txt=None):
    """
    Populates or updates the database with ingredients that are parsed from a
    txt file.
    """
    try:
        with open(ingredients_txt) as f:
            f.readline()
            for line in f:
                line = [item.strip() for item in line.split(';')]
                Ingredient.objects.get_or_create(name=line[0].strip(),
                                                 type=line[1].strip(),
                                                 description=line[2].strip())
        print(bcolors.OKBLUE + "Ingredient population is done." + bcolors.ENDC)
    except (FileNotFoundError, TypeError):
        print(bcolors.FAIL +
              "Input file was not recognized. Please check your input." +
              bcolors.ENDC)


def populate_recipes():
    """
    Populate the database with recipe instances.
    """

    pass

if __name__ == '__main__':
    units_file = 'data/units.txt'
    ingredients_file = 'data/ingredients.txt'
    populate_units(units_txt=units_file)
    populate_ingredients(ingredients_txt=ingredients_file)

