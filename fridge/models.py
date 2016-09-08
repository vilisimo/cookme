from django.db import models
from django.urls import reverse

from django.contrib.auth.models import User

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