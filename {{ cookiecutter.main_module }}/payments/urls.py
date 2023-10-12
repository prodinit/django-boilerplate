# Third Party Stuff
from rest_framework.routers import SimpleRouter
from django.urls import path, include

from users.views import AuthViewSet

default_router = SimpleRouter(trailing_slash=False)

# default_router.register(r"", ViewSet, basename="payments")
urlpatterns = [
    # path(
    #     "<str:transaction_id>",
    #     ViewSet.as_view(),
    #     name="get_transaction_",
    # ),
]
urlpatterns += default_router.urls