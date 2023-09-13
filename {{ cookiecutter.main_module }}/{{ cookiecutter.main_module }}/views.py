from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

class HealthViewSet(viewsets.ViewSet):
    """
    A simple healthcheck ViewSet for load balancers.
    """
    def list(self, request):
        pass
    
    @action(methods=['get'], detail=False, permission_classes=[], url_path='health')
    def health(self, request, *args, **kwargs):
        return Response(status=200)
