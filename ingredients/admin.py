from django.contrib import admin
from .models import Ingredient, Unit


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'id')


class UnitAdmin(admin.ModelAdmin):
    list_display = ('abbrev', 'unit', 'description', '__str__')


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Unit, UnitAdmin)

