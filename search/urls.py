from django.conf.urls import url

from .views import search_results

urlpatterns = [
    url(r'^$', search_results, name='search_results'),
]
