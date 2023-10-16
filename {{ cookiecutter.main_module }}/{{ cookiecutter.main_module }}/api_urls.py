# Third Party Stuff
from rest_framework.routers import SimpleRouter
from django.urls import path, include

from .views import HealthViewSet

default_router = SimpleRouter(trailing_slash=False)
default_router.register(r"", HealthViewSet, basename="health")

# Combine urls from both default and singleton routers and expose as
# 'urlpatterns' which django can pick up from this module.
urlpatterns = default_router.urls

urlpatterns += [
    # Register all your urls here
    path("", include("users.urls"), name="users"),
    path("", include("payments.urls"), name="payments")
    # path("", include("slack_notification.urls"))
    # path("", include("whatsapp_notification.urls"))
]
