from django.contrib import admin

from .models import Fridge, FridgeIngredient


class FridgeAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__', 'ingredient_list')
    list_display_links = ('__str__',)

    def ingredient_list(self, obj):
        return ", ".join([ingredient.name for ingredient in
                          obj.ingredients.all()])


class FridgeIngredientAdmin(admin.ModelAdmin):
    list_display = ('fridge', 'ingredient', 'unit', 'quantity')


admin.site.register(Fridge, FridgeAdmin)
admin.site.register(FridgeIngredient, FridgeIngredientAdmin)

