from django.conf.urls import url

from .views import (
    recipes,
    recipe_detail
)

urlpatterns = [
    url(r'^$', recipes, name='recipes'),
    url(r'^(?P<slug>[\w\-]+)/$', recipe_detail, name='recipe_detail'),
]
