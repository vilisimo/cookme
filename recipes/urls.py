from django.conf.urls import url
from recipes import views

urlpatterns = [
	url(r'^$', views.recipes, name='recipes'),
	url(r'^test/', views.test, name='test'),
]
