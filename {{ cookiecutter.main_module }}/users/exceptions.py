from rest_framework import exceptions
from django.utils.translation import gettext_lazy as _

class UnableToSendActivationEmail(Exception):
    pass

class UnableToSendPasswordResetEmail(Exception):
    pass

class UnableToSendOTP(Exception):
    pass

class InvalidLoginArguments(Exception):
    pass

class BaseException(exceptions.APIException):
    default_detail = _("Unexpected error")

    def __init__(self, detail=None):
        self.detail = detail or self.default_detail

class NotAuthenticated(exceptions.NotAuthenticated):
    """Compatibility subclass of restframework `NotAuthenticated` exception."""
    pass

class BadRequest(BaseException):
    """Exception used on bad arguments detected on api view."""
    default_detail = _("Wrong arguments.")

class RequestValidationError(BadRequest):
    default_detail = _("Data validation error")