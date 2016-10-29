from django.test import TestCase
from django.contrib.auth.models import User

from ingredients.models import Unit, Ingredient
from recipes.models import Recipe, RecipeIngredient as RecIng
from fridge.helpers import get_fridge_recipes


class TestGetRecipes(TestCase):
    """
    Test cases to ensure that matching recipes against a given ingredient set
    returns an expected result.
    """

    def setUp(self):
        user = User.objects.create(username='get_fridge_recipes')

        # Ingredients
        i1 = Ingredient.objects.create(name='Meat', type='Meat')
        i2 = Ingredient.objects.create(name='Lemon', type='Fruit')
        i3 = Ingredient.objects.create(name='Apple', type='Fruit')
        i4 = Ingredient.objects.create(name='White Bread', type='Bread')
        # Units
        u = Unit.objects.create(name='kilogram', abbrev='kg')

        # Recipes
        self.r = Recipe.objects.create(author=user, title='MeatRec')
        RecIng.objects.create(recipe=self.r, ingredient=i1, unit=u, quantity=1)

        self.r2 = Recipe.objects.create(author=user, title='MeatLemonAppleRec')
        RecIng.objects.create(recipe=self.r2, ingredient=i1, unit=u, quantity=1)
        RecIng.objects.create(recipe=self.r2, ingredient=i2, unit=u, quantity=1)
        RecIng.objects.create(recipe=self.r2, ingredient=i3, unit=u, quantity=1)

        self.r3 = Recipe.objects.create(author=user, title="AllIngredientsRec")
        RecIng.objects.create(recipe=self.r3, ingredient=i1, unit=u, quantity=1)
        RecIng.objects.create(recipe=self.r3, ingredient=i2, unit=u, quantity=1)
        RecIng.objects.create(recipe=self.r3, ingredient=i3, unit=u, quantity=1)
        RecIng.objects.create(recipe=self.r3, ingredient=i4, unit=u, quantity=1)

        self.r4 = Recipe.objects.create(author=user, title="LemonRec")
        RecIng.objects.create(recipe=self.r4, ingredient=i2, unit=u, quantity=1)

    def test_get_recipes_one_ingredient(self):
        """
        Ensures that when only one ingredient is given, only a recipe
        with that one ingredient is returned.
        """

        ingredients = {'meat'}
        recipes = get_fridge_recipes(ingredients)

        self.assertIn(self.r, recipes)

    def test_get_recipes_two_ingredients(self):
        """
        Ensures that when we there are two ingredients in a set, only those
        recipes that consist of one ingredient or both of them are returned.
        """

        ingredients = {'meat', 'lemon'}
        recipes = get_fridge_recipes(ingredients)
        expected = [self.r, self.r4]

        self.assertEquals(expected, list(recipes))

    def test_get_recipes_all_ingredients(self):
        """
        Ensures that all recipes are chosen when ingredient list includes all
        possible ingredients.
        """

        ingredients = {'meat', 'lemon', 'apple', 'white bread'}
        recipes = get_fridge_recipes(ingredients)
        expected = Recipe.objects.all()

        self.assertEquals(list(expected), list(recipes))

    def test_non_existent_ingredient(self):
        """ Ensure that non-existent ingredients do not return anything. """

        ingredients = {'fairy dust'}
        recipes = get_fridge_recipes(ingredients)

        self.assertFalse(recipes)

