"""
Population scrip that can be run to create an initial, small test database.
Still needs a lot of work, as it is quite fragile.

Note: password for the recipe's author is the same as the author's name. Unsafe.
Note 2: status updates are shown in console only when populate.py is launched
from command line
"""

import os
import sys

import yaml

project_path = os.path.normpath(os.getcwd() + os.sep + os.pardir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cookme.settings")
sys.path.append(project_path)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django.db import transaction
from django.core.management import execute_from_command_line
from django.contrib.auth.models import User

from recipes.models import Recipe, RecipeIngredient as RI
from ingredients.models import Ingredient, Unit


class bcolors:
    OKBLUE = '\033[94m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    @staticmethod
    def error(message):
        return f'{bcolors.FAIL}{message}{bcolors.ENDC}'

    @staticmethod
    def success(message):
        return f'{bcolors.OKBLUE}{message}{bcolors.ENDC}'


def terminal_out(message, error=False, terminate=True):
    """
    Mini method to print error/success messages, so that if name=main does
    not have to be repeated over and over again in populate script...

    :param message: error/success message to be printed.
    :param error: determines the output color: success (false) or error (true).
    :param terminate: whether the population script stops after the error.
    """

    if __name__ == '__main__':
        if error:
            print(bcolors.error(message))
            if terminate:
                print(bcolors.error('Population terminated.'))
        else:
            print(bcolors.success(message))
    else:
        pass


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

    execute_from_command_line(['manage.py', 'makemigrations'])
    execute_from_command_line(['manage.py', 'migrate'])
    terminal_out('Migrations were carried out successfully.')


def create_super_user(username):
    """ Creates super user for testing purposes """

    user = _create_user_if_doesnt_exist(username)
    _give_privileges_to(user)

    terminal_out('Super user created successfully.')
    terminal_out(f'Login: {username} \nPassword: {username}')


def _create_user_if_doesnt_exist(username):
    """ Checks if the user exists. If not, creates it with a weak password. """

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = User.objects.create_user(username=username, password=username)
    return user


def _give_privileges_to(user):
    """ Assign admin and staff privileges to given user """

    user.is_superuser = True
    user.is_staff = True
    user.save()


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
                _populate_unit_from_input_line(line)
        terminal_out('Unit population is done.')
    except (FileNotFoundError, TypeError):
        terminal_out('Input file not recognized.', error=True)
        raise


def _populate_unit_from_input_line(line):
    """ Creates a Unit entity using an input line extracted from Units.txt """

    line = [item.strip() for item in line.strip().split(';')]
    # Get or create is used in case we need to update the DB rather
    # than populate it from scratch.
    Unit.objects.get_or_create(name=line[0], abbrev=line[1], plural=line[2], description=line[3])


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
                _populate_ingredient_from_input_line(line)
        terminal_out('Ingredient population is done.')
    except (FileNotFoundError, TypeError):
        terminal_out('Input file was not recognized.', error=True)
        raise


def _populate_ingredient_from_input_line(line):
    """ Creates Ingredient entity from a line of text """

    line = [item.strip() for item in line.split(';')]
    name = line[0].strip()
    ing_type = line[1].strip()
    desc = line[2].strip()
    Ingredient.objects.get_or_create(name=name, type=ing_type, description=desc)


@transaction.atomic
def populate_recipes(recipe_folder=None):
    """
    Populates the database with recipe instances.
    """

    _check_path_exists(recipe_folder)
    _check_not_empty(recipe_folder)

    try:
        # Each file represents a recipe
        files = os.listdir(recipe_folder)
        for index, f in enumerate(files):
            _report_process(index, f, files)
            path = f'{recipe_folder}/{f}'

            # If file is empty - more useful for myself to warn, instead crash
            if os.stat(path).st_size <= 0:
                message = f'File nr.{index+1} is empty.'
                terminal_out(message, error=True, terminate=False)
                continue

            values = yaml.load(open(path, 'r'))
            recipe = commit_recipe(values)

            commit_recipe_ingredient(values, recipe)

        terminal_out('Recipe population is done.')

    except (FileNotFoundError, TypeError):
        terminal_out('Input path was not recognized.', error=True)
        raise

    except User.DoesNotExist:
        terminal_out('Such username does not exist. Please create a user.', error=True)
        raise

    except KeyError as e:
        terminal_out(f"'{e.args[0]}' field was not found. Please ensure that "
                     f"YML file contains it.", error=True)


def _check_path_exists(recipe_folder):
    """ Ensure the given path to folder exists """

    if recipe_folder is None:
        terminal_out('Path was not provided.', error=True)
        raise FileNotFoundError('Path was not provided.')


def _check_not_empty(recipe_folder):
    """ Ensure recipe folder is not empty. Otherwise population is useless"""

    if not os.listdir(recipe_folder):
        terminal_out('Folder is empty. Please add recipes.', error=True)
        raise FileNotFoundError('No files found in the directory.')


def _report_process(index, file_, files):
    """ Report recipe creation process on the console """

    if __name__ == '__main__':
        processed = file_.split('/')[-1]
        print(f'Processing {index+1}/{len(files)} file: {processed}')


def commit_recipe(values):
    """
    Creates a single recipe instance and commits it to the DB.

    :param values: a dictionary of values to be used in recipe
                   (typically from YML).
    :return: Recipe instance
    """

    try:
        a = values['author']
        t = values['title']
        d = values['description']
        c = values['cuisine']
        s = values['steps']
        p = values['picture']

        step_list = []
        for step in s:
            step_list.append(values['steps'][step].strip())

        u = get_user(username=a, password=a)
        recipe = Recipe.objects.get_or_create(author=u, title=t, cuisine=c, description=d,
                                              steps="\n".join(step_list), image=p)[0]
        return recipe
    except KeyError:
        raise


def commit_recipe_ingredient(values, recipe):
    """
    Creates a single ingredient instance and commits it to the database.

    :param values: dictionary of values to be used in RecipeIngredient
                   (typically from YML file).
    :param recipe: Recipe object with which relevant objects are associated.
    :return: List of RecipeIngredient objects.
    """

    try:
        ris = []
        ingredients = values['ingredients']
        for ing in ingredients:
            quantity_unit = values['ingredients'][ing].split()
            quantity = quantity_unit[0]
            unit = Unit.objects.get_or_create(abbrev__iexact=quantity_unit[1])[0]
            ingr = Ingredient.objects.get_or_create(name__iexact=ing)[0]

            ris.append(RI.objects.get_or_create(recipe=recipe, ingredient=ingr,
                                                unit=unit, quantity=quantity))
        return ris
    except KeyError:
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
    create_super_user(username="admin")


