import requests
from oauthlib.common import UNICODE_ASCII_CHARACTER_SET
from random import SystemRandom
from urllib.parse import urlencode

from django.conf import settings
from django.urls import reverse_lazy

from .creds import google_login_get_credentials, GoogleAccessTokens
from users.exceptions import UnableToFetchAccessToken
from users.models import User
from users.choices import GOOGLE


class GoogleLoginFlowService:
    API_URI = reverse_lazy("callback")

    GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
    GOOGLE_ACCESS_TOKEN_OBTAIN_URL = "https://oauth2.googleapis.com/token"
    GOOGLE_AUTH_PROVIDER_CERT_URL = "https://www.googleapis.com/oauth2/v1/certs"
    GOOGLE_USER_INFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

    SCOPES = [
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
        "openid",
    ]

    def __init__(self):
        self._credentials = google_login_get_credentials()

    @staticmethod
    def _generate_state_session_token(length=30, chars=UNICODE_ASCII_CHARACTER_SET):
        # This is how it's implemented in the official SDK
        rand = SystemRandom()
        state = "".join(rand.choice(chars) for _ in range(length))
        return state

    def _get_redirect_uri(self):
        domain = settings.DOMAIN
        api_uri = self.API_URI
        redirect_uri = f"{domain}{api_uri}"
        return redirect_uri

    def get_authorization_url(self):
        redirect_uri = self._get_redirect_uri()

        state = self._generate_state_session_token()

        params = {
            "response_type": "code",
            "client_id": self._credentials.client_id,
            "redirect_uri": redirect_uri,
            "scope": " ".join(self.SCOPES),
            "state": state,
            "access_type": "offline",
            "include_granted_scopes": "true",
            "prompt": "select_account",
        }

        query_params = urlencode(params)
        authorization_url = f"{self.GOOGLE_AUTH_URL}?{query_params}"

        return authorization_url, state

    def get_tokens(self, *, code: str) -> GoogleAccessTokens:
        redirect_uri = self._get_redirect_uri()

        data = {
            "code": code,
            "client_id": self._credentials.client_id,
            "client_secret": self._credentials.client_secret,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        }

        response = requests.post(self.GOOGLE_ACCESS_TOKEN_OBTAIN_URL, data=data)

        if not response.ok:
            raise UnableToFetchAccessToken("Failed to obtain access token from Google.")

        tokens = response.json()
        google_tokens = GoogleAccessTokens(
            id_token=tokens["id_token"],
            access_token=tokens["access_token"],
            refresh_token=tokens["refresh_token"],
            token_type=tokens["token_type"],
        )

        return google_tokens

    def get_user_info(self, data: dict) -> User:
        email = data.get("email")
        first_name = data.get("given_name")
        last_name = data.get("family_name")
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return User.objects.create(
                email=email,
                first_name=first_name,
                last_name=last_name,
                is_email_verified=True,
                is_active=True,
                auth_provider=GOOGLE,
            )
