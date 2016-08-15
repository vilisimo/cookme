from django.contrib import admin

from .models import Ingredient, Recipe


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'description', 'date', 'views', 'image')


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type')


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
