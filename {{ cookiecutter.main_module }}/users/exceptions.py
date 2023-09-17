from rest_framework import exceptions

class UnableToSendActivationEmail(Exception):
    pass

class UnableToSendOTP(Exception):
    pass

class InvalidLoginArguments(Exception):
    pass

class NotAuthenticated(exceptions.NotAuthenticated):
    """Compatibility subclass of restframework `NotAuthenticated` exception."""

    pass