from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.shortcuts import redirect

from users.serializers import LoginSerializer, SignupSerializer
from users.services import AuthServices
from users.choices import EMAIL

class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny]

    @action(methods=['POST'], detail=False)
    def login(self, request, *args, **kwargs):
        print(request)
        return Response({}, status=200)
    
    @action(methods=['POST'], detail=False)
    def signup(self, request, *args, **kwargs):
        data = request.data
        serializer = SignupSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = AuthServices.create_user_account(**serializer.validated_data)
        AuthServices.send_account_activation_email(user, template_name="email/account_activation_email.tpl")
        return Response({}, status=200)
    
    @action(methods=['GET'], detail=False)
    def activate(self, request, *args, **kwargs):
        token = request.query_params.get('token')
        if token:
            try:
                user = Token.objects.get(key=token).user
                print(user)
            except Token.DoesNotExist:
                pass
            else:
                user.is_active = True
                user.is_email_verified = True
                user.auth_provider = EMAIL
                user.save()
        return redirect('/')
    
    @action(methods=['POST'], detail=False)
    def logout(self, request, *args, **kwargs):
        print(request)
        return Response({}, status=200)
    
    @action(methods=['POST'], detail=False)
    def password_reset(self, request, *args, **kwargs):
        print(request)
        return Response({}, status=200)
    
    @action(methods=['POST'], detail=False)
    def password_change(self, request, *args, **kwargs):
        print(request)
        return Response({}, status=200)
    
    @action(methods=['POST'], detail=False)
    def password_reset_confirm(self, request, *args, **kwargs):
        print(request)
        return Response({}, status=200)