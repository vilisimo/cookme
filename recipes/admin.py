from django.contrib import admin

from .models import Recipe, Rating, RecipeIngredient


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'description', 'steps_display', 'ingredient_list', 'cuisine',
                    'views', 'slug', 'image', 'date',)
    list_display_links = ('title',)
    prepopulated_fields = {"slug": ("title",)}

    def ingredient_list(self, obj):
        return ", ".join([ingredient.name for ingredient in obj.ingredients.all()])

    def steps_display(self, obj):
        st_list = obj.step_list()
        return "; ".join([step for step in st_list])


class RatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe', 'stars', 'date')


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'unit', 'quantity')


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
