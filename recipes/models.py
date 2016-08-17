from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


INGREDIENTS = [
    ('Additives', 'Food additives'),
    ('Condiments', 'Condiments'),
    ('Oils', 'Cooking oils'),
    ('Eggs', 'Eggs'),
    ('Dairy', 'Dairy'),
    ('Flour', 'Flour'),
    ('Fruits', 'Fruits'),
    ('Grains', 'Grains'),
    ('Herbs', 'Herbs'),
    ('Meat', 'Meat'),
    ('Nuts', 'Nuts'),
    ('Pasta', 'Pasta'),
    ('Poultry', 'Poultry'),
    ('Salts', 'Salts'),
    ('Sauces', 'Sauces'),
    ('Seafood', 'Seafood'),
    ('Seeds', 'Seeds'),
    ('Spices', 'Spices'),
    ('Sugars', 'Sugars'),
    ('Vegetables', 'Vegetables'),
]

INGREDIENTS = sorted(INGREDIENTS, key=lambda x: x[1])


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Ingredient(models.Model):
    """    Model that represents ingredients of recipes.    """
    name = models.CharField(max_length=250, null=False)
    type = models.CharField(max_length=250, null=False, choices=INGREDIENTS)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """    Model that represents recipes.    """
    author = models.ForeignKey(User)
    title = models.CharField(max_length=250, null=False)
    description = models.TextField()
    ingredients = models.ManyToManyField(Ingredient)
    date = models.DateTimeField(editable=False)
    views = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='recipes/',
                              default='recipes/no-image.jpg')

    def ingredient_list(self):
        return ", ".join([str(ingredient) for ingredient in
                          self.ingredients.all()])

    def save(self, *args, **kwargs):
        """ Date is updated only when model is saved """
        if not self.id:
            self.date = timezone.now()
        return super(Recipe, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


# Note: there are rating packages for Django, but more fun to create it from 0.
class Rating(models.Model):
    """ Model representing ratings that can be made. """
    stars = models.IntegerField(validators=[MinValueValidator(1),
                                MaxValueValidator(5)])
    user = models.OneToOneField(User)
    recipe = models.ForeignKey(Recipe, blank=False, null=False)
    date = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        """ Date is updated only when model is saved """
        if not self.id:
            self.date = timezone.now()
        return super(Rating, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.user) + \
               '\'s ' + str(self.recipe) + ' rating: {0}'.format(self.stars)


class Fridge(models.Model):
    """ Model representing fridge (collection of recipes & ingredients). """
    user = models.OneToOneField(User)
    recipes = models.ManyToManyField(Recipe)
    ingredients = models.ManyToManyField(Ingredient)

    def recipe_list(self):
        return ", ".join([str(recipe) for recipe in self.recipes.all()])

    def ingredient_list(self):
        return ", ".join([str(ingredient) for ingredient in
                          self.ingredients.all()])

    def __str__(self):
        return str(self.user) + '\'s fridge'
