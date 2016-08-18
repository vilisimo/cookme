from django.contrib import admin

from .models import Ingredient, Recipe, Rating, Fridge, Unit
from .models import FridgeIngredient, RecipeIngredient


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'description', 'date', 'views', 'image')


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'id')


class FridgeAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__')


class RatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe', 'stars', 'date')


class UnitAdmin(admin.ModelAdmin):
    list_display = ('abbrev', 'unit', 'description', '__str__')


class FridgeIngredientAdmin(admin.ModelAdmin):
    list_display = ('fridge', 'ingredient', 'unit', 'quantity')


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'unit', 'quantity')


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Fridge, FridgeAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(FridgeIngredient, FridgeIngredientAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
