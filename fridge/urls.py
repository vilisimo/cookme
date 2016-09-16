from django.conf.urls import url

from .views import (
    fridge_detail,
    add_recipe,
)

urlpatterns = [
    url(r'^$', fridge_detail, name='fridge_detail'),
    url(r'add_recipe/$', add_recipe, name='add_recipe'),
]