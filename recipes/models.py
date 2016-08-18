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
    name = models.CharField(max_length=250, null=False, unique=True)
    type = models.CharField(max_length=250, null=False, choices=INGREDIENTS)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """    Model that represents recipes.    """
    author = models.ForeignKey(User)
    title = models.CharField(max_length=250, null=False)
    description = models.TextField()
    date = models.DateTimeField(editable=False)
    views = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='recipes/',
                              default='recipes/no-image.jpg')

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


# May not be needed. May be possible to go through user and create illusion
# of fridge. However, having Fridge entity allows multiple fridges if needed.
class Fridge(models.Model):
    """ Model representing fridge (collection of recipes & ingredients). """
    user = models.OneToOneField(User)

    def __str__(self):
        return str(self.user) + '\'s fridge'


class Unit(models.Model):
    """ Model representing quantities, such as oz, kg, ml, etc. """
    unit = models.CharField(max_length=30, blank=False, null=False, unique=True)
    abbrev = models.CharField(max_length=5, blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return "{0} ({1})".format(self.unit, self.abbrev)


class FridgeIngredient(models.Model):
    """
    Model representing ingredients in the fridge. Note on quantity: users may
    not necessarily know how much of an ingredient they have.
    """
    fridge = models.ForeignKey(Fridge)
    ingredient = models.ForeignKey(Ingredient)
    unit = models.ForeignKey(Unit, blank=True, null=True)
    quantity = models.FloatField(blank=True, null=True)

    class Meta:
        unique_together = ('fridge', 'ingredient')

    def __str__(self):
        return "{0} in {1}".format(self.ingredient, self.fridge)


class RecipeIngredient(models.Model):
    """ Model representing ingredients in the recipe. Quantity is a must! """
    recipe = models.ForeignKey(Recipe)
    ingredient = models.ForeignKey(Ingredient)
    unit = models.ForeignKey(Unit, blank=False, null=False)
    quantity = models.FloatField(blank=False, null=False)

    class Meta:
        unique_together = ('recipe', 'ingredient')

    def __str__(self):
        return "{0} in {1}".format(self.ingredient, self.recipe)
