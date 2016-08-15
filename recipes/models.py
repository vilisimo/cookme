from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User
# from django.core.validators import MinValueValidator, MaxValueValidator


INGREDIENTS = (
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
)


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


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


class Ingredient(models.Model):
    """    Model that represents ingredients of recipes.    """
    name = models.CharField(max_length=250, null=False)
    type = models.CharField(max_length=250, null=False, choices=INGREDIENTS)

    def __str__(self):
        return self.name


# Should I just use already existing packages? Good: easy; tested, etc. Bad:
# won't learn anything; everything's done for me.
# class Rating(models.Model):
#     """
#     Model representing the ratings that can be made.
#     """
#     stars = models.IntegerField(MinValueValidator(1), MaxValueValidator(5))
#     user = models.ForeignKey(User, unique=True)


