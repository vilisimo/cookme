from django.conf.urls import url

from .views import (
    fridge_detail,
    add_recipe,
    remove_ingredient,
    remove_recipe,
    possibilities,
    fridge_recipes,
)

urlpatterns = [
    url(r'^$', fridge_detail, name='fridge_detail'),
    url(r'possibilities/$', possibilities, name='possibilities'),
    url(r'fridge_recipes/', fridge_recipes, name='fridge_recipes'),
    url(r'add_recipe/$', add_recipe, name='add_recipe'),
    url(r'remove_ingredient/(?P<pk>\d+)/$', remove_ingredient, name='remove_ingredient'),
    url(r'remove_recipe/(?P<pk>\d+)/$', remove_recipe, name='remove_recipe'),

]
