# Third Party Stuff
from rest_framework.routers import SimpleRouter
from .views import HealthViewSet

default_router = SimpleRouter(trailing_slash=False)

# Register all the django rest framework viewsets below.
default_router.register(r"", HealthViewSet, basename="health")

# Combine urls from both default and singleton routers and expose as
# 'urlpatterns' which django can pick up from this module.
urlpatterns = default_router.urls
