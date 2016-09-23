from string import capwords

from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Ingredient(models.Model):
    """ Model that represents ingredients of recipes. """

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
        ('Paste', 'Paste'),
        ('Poultry', 'Poultry'),
        ('Salts', 'Salts'),
        ('Sauces', 'Sauces'),
        ('Seafood', 'Seafood'),
        ('Seeds', 'Seeds'),
        ('Spices', 'Spices'),
        ('Sugars', 'Sugars'),
        ('Vegetables', 'Vegetables'),
        ('Unspecified', 'Unspecified'),
    ]
    INGREDIENTS = sorted(INGREDIENTS, key=lambda x: x[1])

    name = models.CharField(max_length=250, null=False, unique=True)
    type = models.CharField(max_length=250, blank=True, null=False,
                            default='Unspecified', choices=INGREDIENTS)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        """
        Even though name is unique, slug may be not unique. For example,
        if model 1 has name ';a;' and model 2 has name ';a:'. In such a case,
        slug would be 'a' for both.
        """

        if not self.id:
            slug = slugify(self.name)
            i = 2
            while Ingredient.objects.filter(slug=slug):
                slug = "{0}-{1}".format(slug, i)
                i += 1
            self.slug = slug
            self.name = capwords(self.name)
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
    abbrev = models.CharField(max_length=10, blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.abbrev
