from rest_framework import serializers
from django.contrib.auth import password_validation
from django.contrib.auth.models import BaseUserManager

from users.validators import phone_regex

from users.models import User

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True)

class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False, validators=[phone_regex])
    username = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    password = serializers.CharField(required=True)

    def validate(self, value):
        if "email" not in value and "phone_number" not in value:
            raise serializers.ValidationError("Email or Phone Number required")
        return value
    
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
