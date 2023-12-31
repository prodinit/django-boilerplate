from rest_framework import serializers
from django.contrib.auth import password_validation
from django.contrib.auth.models import BaseUserManager

from users.validators import phone_regex
from users.tokens import get_token_for_user
from users.models import User


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "phone_number"]


class AuthUserSerializer(UserSerializer):
    auth_token = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ["auth_token"]

    def get_auth_token(self, value):
        return get_token_for_user(value, "authentication")


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    phone_number = serializers.CharField(required=False, validators=[phone_regex])
    username = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    password = serializers.CharField(required=True)

    def validate_email(self, value):
        if value and User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Email is already taken.")
        return value.strip()

    def validate_phone_number(self, value):
        if value and User.objects.filter(phone_number__iexact=value).exists():
            raise serializers.ValidationError("Phone Number is already taken.")
        return value

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    token = serializers.CharField(required=True)

    def validate_new_password(self, value):
        password_validation.validate_password(value)
        return value


class PasswordChangeSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        password_validation.validate_password(value)
        return value
