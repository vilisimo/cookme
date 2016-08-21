from django.contrib import admin

from .models import Fridge, FridgeIngredient


class FridgeAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__')


class FridgeIngredientAdmin(admin.ModelAdmin):
    list_display = ('fridge', 'ingredient', 'unit', 'quantity')


admin.site.register(Fridge, FridgeAdmin)
admin.site.register(FridgeIngredient, FridgeIngredientAdmin)

