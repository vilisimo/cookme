from django.conf.urls import url

from .views import (
    fridge_detail,
)

urlpatterns = [
    url(r'^$', fridge_detail, name='fridge_detail'),
]