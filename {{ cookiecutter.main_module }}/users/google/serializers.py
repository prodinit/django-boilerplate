import logging

from rest_framework import serializers

from users.exceptions import (
    InvalidGoogleAuthCode,
    InvalidGoogleAuthState,
    GoogleAuthError,
)

logger = logging.getLogger(__name__)


class GoogleLoginSerializer(serializers.Serializer):
    code = serializers.CharField(required=False)
    error = serializers.CharField(required=False)
    state = serializers.CharField(required=False)

    def validate_error(self, value):
        raise GoogleAuthError(detail=value)

    def validate_code(self, value):
        if not value:
            logger.info(f"Invalid google code {value}")
            raise InvalidGoogleAuthCode
        return value

    def validate_state(self, value):
        if not value:
            logger.info(f"Invalid google state {value}")
            raise InvalidGoogleAuthState
        return value
