import os
import sys

project_path = os.path.normpath(os.getcwd() + os.sep + os.pardir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cookme.settings")
sys.path.append(project_path)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django.db import transaction
from django.contrib.auth.models import User

from recipes.models import Recipe, RecipeIngredient
from ingredients.models import Ingredient, Unit


class bcolors:
    OKBLUE = '\033[94m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


@transaction.atomic
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


@transaction.atomic
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


@transaction.atomic
def populate_recipes(recipe_folder=None):
    """
    Populate the database with recipe instances.
    """

    import yaml

    if recipe_folder is None:
        print(bcolors.FAIL + "Path was not provided." + bcolors.ENDC)
        return

    try:
        # Each file represents a recipe
        files = os.listdir(recipe_folder)
        for index, f in enumerate(files):
            print("Processing {}/{} file...".format(index+1, len(files)))

            path = "{}/{}".format(recipe_folder, f)
            values = yaml.load(open(path, 'r'))

            # First create a recipe
            author = values['author']
            title = values['title']
            description = values['description']
            cuisine = values['cuisine']
            steps = values['steps']
            step_list = []
            for step in steps:
                step_list.append(values['steps'][step].strip())

            admin = User.objects.get(username=author)
            recipe, c = Recipe.objects.get_or_create(author=admin, title=title,
                                                     cuisine=cuisine,
                                                     description=description,
                                                     steps="\n".join(step_list))
            # If recipe already in db, exit current iteration
            if not c:
                continue

            # Now create RecipeIngredient with appropriate FKs
            ingredients = values['ingredients']
            for ing in ingredients:
                quantity_unit = values['ingredients'][ing].split()
                quantity = quantity_unit[0]
                unit = Unit.objects.get_or_create(abbrev__iexact=
                                                  quantity_unit[1])[0]
                ingr = Ingredient.objects.get_or_create(name__iexact=ing)[0]

                RecipeIngredient.objects.create(recipe=recipe,
                                                ingredient=ingr,
                                                unit=unit,
                                                quantity=quantity)

        print(bcolors.OKBLUE + "Recipe population is done." + bcolors.ENDC)

    except (FileNotFoundError, TypeError):
        print(bcolors.FAIL +
              "Input path was not recognized. Please check your input." +
              bcolors.ENDC)

    except User.DoesNotExist:
        print(bcolors.FAIL +
              "Such username does not exist. Please create a user." +
              bcolors.ENDC)


if __name__ == '__main__':
    units_file = 'data/units.txt'
    ingredients_file = 'data/ingredients.txt'
    recipes_path = 'data/recipes'
    populate_units(units_txt=units_file)
    populate_ingredients(ingredients_txt=ingredients_file)
    # Admin should be created before calling this function
    populate_recipes(recipe_folder=recipes_path)
