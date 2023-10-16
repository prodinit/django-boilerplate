from django.urls import path

from .api import (
    GoogleLoginCallbackApi,
    GoogleLoginRedirectApi,
)

urlpatterns = [
    path("callback/", GoogleLoginCallbackApi.as_view(), name="callback"),
    path("redirect/", GoogleLoginRedirectApi.as_view(), name="redirect"),
]
