import logging

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from django.shortcuts import redirect
from django.contrib.auth import authenticate, logout

from users.serializers import (
    LoginSerializer,
    SignupSerializer,
    AuthUserSerializer,
    PasswordResetSerializer,
    PasswordResetConfirmSerializer,
    PasswordChangeSerializer,
)
from users.services import AuthServices
from users.models import User
from users.tokens import get_user_for_password_reset_token
from users.exceptions import (
    UnableToSendOTP,
    UnableToSendActivationEmail,
    InvalidLoginArguments,
    UnableToSendPasswordResetEmail,
)

logger = logging.getLogger(__name__)


class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny]

    @action(methods=["POST"], detail=False)
    def login(self, request, *args, **kwargs):
        json_response = {
            "success": True,
            "status_code": status.HTTP_200_OK,
            "message": "Login Successful",
            "error": None,
            "data": None,
        }

        try:
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = authenticate(
                username=serializer.validated_data["email"],
                password=serializer.validated_data["password"],
            )
            if user is None:
                raise InvalidLoginArguments(
                    "Invalid username/password. Please try again!"
                )
            data = AuthUserSerializer(user).data
            json_response["data"] = data
        except ValidationError as ex:
            for error in ex.__dict__["detail"]:
                err_msg = ex.__dict__["detail"][error][0]
                json_response["error"] = f"{error}: {err_msg}"
                break
            json_response["success"] = False
            json_response["message"] = "Validation Failed"
            json_response["status_code"] = status.HTTP_400_BAD_REQUEST
        except InvalidLoginArguments as ex:
            json_response["success"] = False
            json_response["status_code"] = status.HTTP_400_BAD_REQUEST
            json_response["message"] = "Login Failed"
            json_response["error"] = f"{ex}"
        except Exception as ex:
            json_response["success"] = False
            json_response["status_code"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            json_response["message"] = f"Something went wrong"
            json_response["error"] = f"{ex}"
        return Response(json_response, status=json_response["status_code"])

    @action(methods=["POST"], detail=False)
    def signup(self, request, *args, **kwargs):
        json_response = {
            "success": True,
            "status_code": status.HTTP_200_OK,
            "message": "Verify you email to activate your account",
            "error": None,
            "data": None,
        }

        try:
            serializer = SignupSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = AuthServices.create_user_account(**serializer.validated_data)
            AuthServices.send_account_activation_email(
                user, template_name="email/account_activation_email.tpl"
            )
        except UnableToSendActivationEmail as ex:
            logger.info(f"Exception occured: {ex}")
            json_response["success"] = False
            json_response["status_code"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            json_response["message"] = f"Unable to send activation Email"
            json_response["error"] = f"{ex}"
        except UnableToSendOTP as ex:
            logger.info(f"Exception occured: {ex}")
            json_response["success"] = False
            json_response["status_code"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            json_response["message"] = f"Unable to OTP"
            json_response["error"] = f"{ex}"
        except ValidationError as ex:
            for error in ex.__dict__["detail"]:
                err_msg = ex.__dict__["detail"][error][0]
                json_response["error"] = f"{error}: {err_msg}"
                break
            json_response["success"] = False
            json_response["message"] = "Validation Failed"
            json_response["status_code"] = status.HTTP_400_BAD_REQUEST
        except Exception as ex:
            logger.info(f"Exception occured for user email {user.id}: {ex}")
            json_response["success"] = False
            json_response["status_code"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            json_response["message"] = f"Something went wrong"
            json_response["error"] = f"{ex}"
        return Response(json_response, status=json_response["status_code"])

    @action(methods=["GET"], detail=False)
    def activate(self, request, *args, **kwargs):
        token = request.query_params.get("token")
        if token:
            try:
                user = Token.objects.get(key=token).user
            except Token.DoesNotExist as ex:
                logger.info(f"Account Activation Failed: {ex}")
            else:
                user.is_active = True
                user.is_email_verified = True
                user.save()
        logger.info(f"Account Activated for user: {user.email}")
        return redirect("/")

    @action(methods=["POST"], detail=False, permission_classes=[IsAuthenticated])
    def logout(self, request, *args, **kwargs):
        json_response = {
            "success": True,
            "status_code": status.HTTP_200_OK,
            "message": "Logout Successful",
            "error": None,
            "data": None,
        }
        try:
            logout(request)
        except Exception as ex:
            json_response["success"] = False
            json_response["status_code"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            json_response["message"] = f"Something went wrong"
            json_response["error"] = f"{ex}"
        return Response(json_response, status=json_response["status_code"])

    @action(methods=["POST"], detail=False)
    def password_reset(self, request, *args, **kwargs):
        json_response = {
            "success": True,
            "status_code": status.HTTP_200_OK,
            "message": "Further instructions will be sent to the email if it exists",
            "error": None,
            "data": None,
        }
        try:
            import pdb

            pdb.set_trace()
            serializer = PasswordResetSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = User.objects.filter(
                email__iexact=serializer.validated_data["email"]
            ).first()
            if user:
                AuthServices.send_password_reset_mail(user)
        except ValidationError as ex:
            for error in ex.__dict__["detail"]:
                err_msg = ex.__dict__["detail"][error][0]
                json_response["error"] = f"{error}: {err_msg}"
                break
            json_response["success"] = False
            json_response["message"] = "Validation Failed"
            json_response["status_code"] = status.HTTP_400_BAD_REQUEST
        except UnableToSendPasswordResetEmail as ex:
            logger.info(f"Exception occured: {ex}")
            json_response["success"] = False
            json_response["status_code"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            json_response["message"] = f"Unable to send password reset email"
            json_response["error"] = f"{ex}"
        except Exception as ex:
            json_response["success"] = False
            json_response["status_code"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            json_response["message"] = f"Something went wrong"
            json_response["error"] = f"{ex}"

        return Response(json_response, status=json_response["status_code"])

    @action(methods=["POST"], detail=False, permission_classes=[IsAuthenticated])
    def password_change(self, request, *args, **kwargs):
        json_response = {
            "success": True,
            "status_code": status.HTTP_200_OK,
            "message": "Password change successful",
            "error": None,
            "data": None,
        }

        try:
            serializer = PasswordChangeSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            request.user.set_password(serializer.validated_data["new_password"])
            request.user.save()
        except ValidationError as ex:
            for error in ex.__dict__["detail"]:
                err_msg = ex.__dict__["detail"][error][0]
                json_response["error"] = f"{error}: {err_msg}"
                break
            json_response["success"] = False
            json_response["message"] = "Validation Failed"
            json_response["status_code"] = status.HTTP_400_BAD_REQUEST
        except Exception as ex:
            json_response["success"] = False
            json_response["status_code"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            json_response["message"] = f"Something went wrong"
            json_response["error"] = f"{ex}"

        return Response(json_response, status=json_response["status_code"])

    @action(methods=["POST"], detail=False)
    def password_reset_confirm(self, request, *args, **kwargs):
        try:
            json_response = {
                "success": True,
                "status_code": status.HTTP_200_OK,
                "message": "Password Reset successful",
                "error": None,
                "data": None,
            }
            serializer = PasswordResetConfirmSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = get_user_for_password_reset_token(serializer.validated_data["token"])
            user.set_password(serializer.validated_data["new_password"])
            user.save()
        except ValidationError as ex:
            for error in ex.__dict__["detail"]:
                err_msg = ex.__dict__["detail"][error][0]
                json_response["error"] = f"{error}: {err_msg}"
                break
            json_response["success"] = False
            json_response["message"] = "Validation Failed"
            json_response["status_code"] = status.HTTP_400_BAD_REQUEST
        except Exception as ex:
            json_response["success"] = False
            json_response["status_code"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            json_response["message"] = f"Something went wrong"
            json_response["error"] = f"{ex}"

        return Response(json_response, status=json_response["status_code"])
