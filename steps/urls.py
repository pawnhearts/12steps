"""steps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.flatpages.views import flatpage
from django.urls import path, include, re_path

urlpatterns = [
    path('', include('guide.urls')),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('accounts/', include('django_registration.backends.one_step.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path("select2/", include("django_select2.urls")),
    path('tinymce/', include('tinymce.urls')),
    path("admin/", admin.site.urls),
    path('api/', include('guide.api.urls')),
    path('', flatpage, {'url': '/'}, name='index'),
    re_path(r'^(?P<url>.*/)$', flatpage),
]
