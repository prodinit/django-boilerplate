# Third Party Stuff
from rest_framework.routers import SimpleRouter
from django.urls import path, include

from users.views import AuthViewSet
from users.google.urls import urlpatterns as ulp

default_router = SimpleRouter(trailing_slash=False)

default_router.register(r"", AuthViewSet, basename="auth")

# Combine urls from both default and singleton routers and expose as
# 'urlpatterns' which django can pick up from this module.
urlpatterns = [path("google/", include(ulp), name="google")]
urlpatterns += default_router.urls
