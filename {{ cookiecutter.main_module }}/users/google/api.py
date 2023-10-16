from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import login

from .services import GoogleLoginFlowService
from .serializers import GoogleLoginSerializer
from users.exceptions import (
    GoogleAuthError,
    InvalidGoogleAuthCode,
    InvalidGoogleAuthState,
    GoogleLoginSessionError,
)
from users.models import User
from users.serializers import AuthUserSerializer


class GoogleLoginRedirectApi(APIView):
    authentication_classes = ()
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        google_login_flow = GoogleLoginFlowService()
        authorization_url, state = google_login_flow.get_authorization_url()
        request.session["google_oauth2_state"] = state
        return redirect(authorization_url)


class GoogleLoginCallbackApi(APIView):
    authentication_classes = ()
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        json_response = {
            "success": True,
            "status_code": status.HTTP_200_OK,
            "message": "Login Successful",
            "error": None,
            "data": None,
        }
        try:
            serializer = GoogleLoginSerializer(data=request.GET)
            serializer.is_valid(raise_exception=True)
            validated_data = serializer.validated_data

            code = validated_data.get("code")
            state = validated_data.get("state")

            session_state = request.session.get("google_oauth2_state")
            if session_state is None or state != session_state:
                raise GoogleLoginSessionError(
                    detail=f"CSRF check failed. Session state: {session_state}. State: {state}"
                )
            del request.session["google_oauth2_state"]

            google_login_flow = GoogleLoginFlowService()
            google_tokens = google_login_flow.get_tokens(code=code)
            id_token_decoded = google_tokens.decode_id_token()

            user = google_login_flow.get_user_info(data=id_token_decoded)
            login(request, user)
            data = AuthUserSerializer(user).data
            json_response["data"] = data
        except GoogleAuthError as ex:
            json_response["success"] = False
            json_response["status_code"] = status.HTTP_400_BAD_REQUEST
            json_response["message"] = "Login Failed"
            json_response["error"] = f"{ex}"
        except (InvalidGoogleAuthCode, InvalidGoogleAuthState):
            json_response["success"] = False
            json_response["status_code"] = status.HTTP_400_BAD_REQUEST
            json_response["message"] = "Login Failed"
            json_response["error"] = "Code and state are required"
        except GoogleLoginSessionError as ex:
            json_response["success"] = False
            json_response["status_code"] = status.HTTP_400_BAD_REQUEST
            json_response["message"] = "Login Failed"
            json_response["error"] = f"{ex}"
        except User.DoesNotExist:
            json_response["success"] = False
            json_response["status_code"] = status.HTTP_400_BAD_REQUEST
            json_response["message"] = "Login Failed"
            json_response["error"] = f"User Does Not Exist"
        except Exception as ex:
            json_response["success"] = False
            json_response["status_code"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            json_response["message"] = f"Something went wrong"
            json_response["error"] = f"{ex}"
        return Response(json_response, status=json_response["status_code"])
