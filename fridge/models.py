from django.db import models
from django.urls import reverse

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

from ingredients.models import Ingredient, Unit
from recipes.models import Recipe


# May not be needed. May be possible to go through user and create illusion
# of fridge. However, having Fridge entity allows multiple fridges if needed.
class Fridge(models.Model):
    """ Model representing fridge (collection of recipes & ingredients). """

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
    Model representing ingredients in the fridge.

    To make calculations easier, user is required to enter quantities and
    units. Alternative: could offer several search options: exact (with
    quantities), not exact (without, match only on ingredients).
    """

    fridge = models.ForeignKey(Fridge)
    ingredient = models.ForeignKey(Ingredient)
    unit = models.ForeignKey(Unit, blank=False, null=False)
    quantity = models.FloatField(validators=[MinValueValidator(0)],
                                 blank=False, null=False)

    class Meta:
        unique_together = ('fridge', 'ingredient')

    def __str__(self):
        return "{0} in {1}".format(self.ingredient, self.fridge)