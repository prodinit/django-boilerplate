"""
URL configuration for {{ cookiecutter.main_module }} project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
# Standard Library
from typing import TYPE_CHECKING, List, Union

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.urls import URLPattern, URLResolver
from django.views.generic import TemplateView
from .api_urls import urlpatterns

URL = Union[URLPattern, URLResolver]
URLList = List[URL]

urlpatterns: "URLList" = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path("about/", TemplateView.as_view(template_name="pages/about.html"), name="about"),
    path(f"{settings.DJANGO_ADMIN_URL}/", admin.site.urls),
    path("api/", include(urlpatterns))
]

# Django Debug Toolbar
if "debug_toolbar" in settings.INSTALLED_APPS:
    # Third Party Stuff
    import debug_toolbar

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
