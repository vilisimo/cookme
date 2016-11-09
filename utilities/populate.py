"""
Population scrip that can be run to create an initial, small test database.
Still needs a lot of work, as it is quite fragile.

Note: password for the recipe's author is the same as the author's name. Unsafe.
Note 2: status updates are shown in console only when populate.py is launched
from command line
"""

import os
import sys

project_path = os.path.normpath(os.getcwd() + os.sep + os.pardir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cookme.settings")
sys.path.append(project_path)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django.db import transaction
from django.core.management import execute_from_command_line
from django.contrib.auth.models import User

from recipes.models import Recipe, RecipeIngredient
from ingredients.models import Ingredient, Unit


class bcolors:
    OKBLUE = '\033[94m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def get_user(username, password):
    """
    Creates a user with a given username and password.

    Note: there is no way to check whether the passwords match, as you cannot
    retrieve user's password. Hence, when trying to get a user, we cannot
    compare them, and we should not even try.

    Note 2: Because of the above considerations, we cannot use get_or_create,
    as it will try to get the user with username and password combination.
    """

    user = None
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = User.objects.create_user(username=username, password=password)
    finally:
        return user


def migrate():
    """ Prepares database for population by building tables. """

    execute_from_command_line(["manage.py", "makemigrations"])
    execute_from_command_line(["manage.py", "migrate"])
    print(bcolors.OKBLUE + "Migrations were carried out successfully." +
          bcolors.ENDC)


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
        if __name__ == '__main__':
            print(bcolors.OKBLUE + "Unit population is done." + bcolors.ENDC)
    except (FileNotFoundError, TypeError):
        if __name__ == '__main__':
            print(bcolors.FAIL +
                  "Input file was not recognized. Please check your input." +
                  bcolors.ENDC)
        raise


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
        if __name__ == '__main__':
            print(bcolors.OKBLUE + "Ingredient population is done." +
                  bcolors.ENDC)
    except (FileNotFoundError, TypeError):
        if __name__ == '__main__':
            print(bcolors.FAIL +
                  "Input file was not recognized. Please check your input." +
                  bcolors.ENDC)
        raise


@transaction.atomic
def populate_recipes(recipe_folder=None):
    """
    Populate the database with recipe instances.
    """

    import yaml

    if recipe_folder is None:
        if __name__ == '__main__':
            print(bcolors.FAIL + "Path was not provided." + bcolors.ENDC)
        raise FileNotFoundError("Path was not provided.")

    if not os.listdir(recipe_folder):
        if __name__ == '__main__':
            print(bcolors.FAIL + "Folder is empty. Please add recipes." +
                  bcolors.ENDC)
        raise FileNotFoundError("No files found in the directory.")

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

            user = get_user(username=author, password=author)
            recipe, c = Recipe.objects.get_or_create(author=user, title=title,
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
        if __name__ == '__main__':
            print(bcolors.OKBLUE + "Recipe population is done." + bcolors.ENDC)

    except (FileNotFoundError, TypeError):
        if __name__ == '__main__':
            print(bcolors.FAIL +
                  "Input path was not recognized. Please check your input." +
                  bcolors.ENDC)
        raise

    except User.DoesNotExist:
        if __name__ == '__main__':
            print(bcolors.FAIL +
                  "Such username does not exist. Please create a user." +
                  bcolors.ENDC)
        raise


if __name__ == '__main__':
    current = os.path.normpath(os.getcwd())
    units_file = os.path.join(current, 'data', 'units.txt')
    ingredients_file = os.path.join(current, 'data', 'ingredients.txt')
    recipes_path = os.path.join(current, 'data', 'recipes')
    migrate()
    populate_units(units_txt=units_file)
    populate_ingredients(ingredients_txt=ingredients_file)
    populate_recipes(recipe_folder=recipes_path)

