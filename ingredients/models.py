from django.db import models


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


class Ingredient(models.Model):
    """    Model that represents ingredients of recipes.    """
    name = models.CharField(max_length=250, null=False, unique=True)
    type = models.CharField(max_length=250, null=False, choices=INGREDIENTS)

    def __str__(self):
        return self.name


class Unit(models.Model):
    """ Model representing quantities, such as oz, kg, ml, etc. """
    unit = models.CharField(max_length=30, blank=False, null=False, unique=True)
    abbrev = models.CharField(max_length=5, blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return "{0} ({1})".format(self.unit, self.abbrev)
