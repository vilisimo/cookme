from django.conf.urls import url

from .views import results

urlpatterns = [
    url(r'^$', results, name='results'),
]
