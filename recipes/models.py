from django.db import models

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


class Ingredient(models.Model):
    """
    Model representing ingredients of recipes.
    """
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


