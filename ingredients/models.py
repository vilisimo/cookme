from django.db import models
from django.urls import reverse
from django.utils.text import slugify


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
    """ Model that represents ingredients of recipes. """

    name = models.CharField(max_length=250, null=False, unique=True)
    type = models.CharField(max_length=250, null=False, choices=INGREDIENTS)
    description = models.CharField(max_length=500, blank=True, null=True)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        if not self.id:
            slug = slugify(self.name)
            self.slug = slug
        return super(Ingredient, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('ingredients:ingredient_detail', args=[self.slug])

    def __str__(self):
        return self.name


class Unit(models.Model):
    """
    Model representing quantities, such as oz, kg, ml, etc.

    Note that it should also allow inputting blank units, e.g. 5 apples.
    """

    name = models.CharField(max_length=30, blank=False, null=False, unique=True)
    abbrev = models.CharField(max_length=5, blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return "{0} ({1})".format(self.name, self.abbrev)
