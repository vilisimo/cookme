from django.conf.urls import url

from .views import (
    recipes,
    recipe_detail,
    add_to_fridge,
)

urlpatterns = [
    url(r'^$', recipes, name='recipes'),
    url(r'^(?P<slug>[\w\-]+)/$', recipe_detail, name='recipe_detail'),
    url(r'add_to_fridge/(?P<pk>\d+)/$', add_to_fridge, name='add_to_fridge'),
]
