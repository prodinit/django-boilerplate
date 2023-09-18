import re

from rest_framework.authentication import BaseAuthentication

from users.tokens import get_user_for_token


class JWTAuthenticationMixin:
    def get_http_authorization(request):
        auth_rx = re.compile(r"^Bearer (.+)$")
        if request is None or "HTTP_AUTHORIZATION" not in request.META:
            return None

        token_rx_match = auth_rx.search(request.META["HTTP_AUTHORIZATION"])
        if not token_rx_match:
            return None

        token = token_rx_match.group(1)
        return token

    def authenticate(self, request):
        token = JWTAuthenticationMixin.get_http_authorization(request)
        if not token:
            return None

        user = get_user_for_token(token, "authentication")

        return (user, token)

    def authenticate_header(self, request):
        return 'Bearer realm="api"'


class RestJWTAuthentication(JWTAuthenticationMixin, BaseAuthentication):
    """Self-contained stateles authentication implementation that work similar to OAuth2.

    It uses json web tokens (https://github.com/jpadilla/pyjwt) for trust
    data stored in the token.
    """

    pass
