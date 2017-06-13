from django.contrib import admin

from .models import Ingredient, Unit


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'description', 'id', 'slug')
    prepopulated_fields = {'slug': ("name",)}


class UnitAdmin(admin.ModelAdmin):
    list_display = ('abbrev', 'name', 'description', '__str__')


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Unit, UnitAdmin)

