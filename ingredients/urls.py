from django.conf.urls import url

from .views import (
    ingredient_detail,
)

urlpatterns = [
    url(r'(?P<slug>[\w\-]+)/$', ingredient_detail, name='ingredient_detail'),
]