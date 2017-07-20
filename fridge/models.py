from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse

from ingredients.models import Ingredient, Unit
from recipes.models import Recipe


class Fridge(models.Model):
    """
    Represents fridge (collection of recipes & ingredients).

    Note: Fridge model not be needed. It is probably possible to create
    something similar through User/UserProfile and simply create an illusion
    of a fridge. However, having Fridge entity allows multiple fridges if
    needed. Besides, it's clearer.
    """

    user = models.OneToOneField(User)
    visible = models.BooleanField(default=True)
    ingredients = models.ManyToManyField(Ingredient, through='FridgeIngredient')
    recipes = models.ManyToManyField(Recipe)

    def __str__(self):
        return str(self.user) + '\'s fridge'

    def get_absolute_url(self):
        return reverse('fridge:fridge_detail')


class FridgeIngredient(models.Model):
    """
    Represents ingredients in the fridge.

    To make calculations easier, user is required to enter quantities and
    units. Alternative: could offer several search options: exact (with
    quantities), not exact (without, match only on ingredients).

    Interesting problems arise, however: what if you have 2 lemons and the
    recipe requires 500g of them?
    """

    fridge = models.ForeignKey(Fridge)
    ingredient = models.ForeignKey(Ingredient)
    unit = models.ForeignKey(Unit, blank=False, null=False)
    quantity = models.FloatField(validators=[MinValueValidator(0)], blank=False, null=False)

    class Meta:
        unique_together = ('fridge', 'ingredient')

    def __str__(self):
        return f'{self.ingredient} in {self.fridge}'
