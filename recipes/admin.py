from django.contrib import admin

from .models import Ingredient, Recipe, Rating, Fridge


class RecipesInline(admin.TabularInline):
    model = Fridge.recipes.through


class IngredientsInline(admin.TabularInline):
    model = Fridge.ingredients.through


class RecipeIngredientsInline(admin.TabularInline):
    model = Recipe.ingredients.through


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'description', 'ingredient_list',
                    'date', 'views', 'image')
    inlines = [RecipesInline, RecipeIngredientsInline]
    exclude = ('ingredients',)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'id')
    inlines = [IngredientsInline, RecipeIngredientsInline]


class FridgeAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__', 'recipe_list', 'ingredient_list')
    inlines = [RecipesInline, IngredientsInline]
    exclude = ('recipes', 'ingredients')


class RatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe', 'stars', 'date')


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Fridge, FridgeAdmin)
admin.site.register(Rating, RatingAdmin)
