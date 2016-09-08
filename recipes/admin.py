from django.contrib import admin

from .models import Recipe, Rating, RecipeIngredient


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'description', 'ingredient_list', 'date',
                    'views', 'slug', 'image')
    prepopulated_fields = {"slug": ("title",)}

    def ingredient_list(self, obj):
        return ", ".join([ingredient.name for ingredient in \
                          obj.ingredients.all()])


class RatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe', 'stars', 'date')


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'unit', 'quantity')


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
