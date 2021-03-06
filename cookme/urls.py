"""cookme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views

from .views import home, register, about

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^about/$', about, name='about'),
    # Needed authentication views. Minimal amount; intentionally so.
    url('^accounts/login/$', auth_views.login,
        kwargs={'redirect_authenticated_user': True}, name='login'),
    url('^accounts/logout/$', auth_views.logout, name='logout'),
    url('^accounts/register/$', register, name='register'),

    # Apps
    url(r'^recipes/', include('recipes.urls', namespace='recipes')),
    url(r'^ingredients/', include('ingredients.urls', namespace='ingredients')),
    url(r'^fridge/', include('fridge.urls', namespace='fridge')),
    url(r'^search/', include('search.urls', namespace='search')),

    # Admin
    url(r'^admin/', admin.site.urls),
    # Should NOT be used in production environment.
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
