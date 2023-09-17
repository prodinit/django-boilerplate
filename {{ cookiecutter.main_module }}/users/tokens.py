import jwt 

from django.conf import settings
from django.contrib.auth import get_user_model

from users.exceptions import NotAuthenticated

HS256_ALGORITHM = "HS256"


def get_token_for_user(user, scope: str) -> str:
    """Generate a new signed token containing a specified user limited for a scope (identified as a string)."""
    data = {"user_%s_id" % (scope): str(user.id)}
    return jwt.encode(data, settings.SECRET_KEY, algorithm=HS256_ALGORITHM)

def get_user_for_token(token: str, scope: str):
    """
    Given a selfcontained token and a scope try to parse and
    unsign it.

    If max_age is specified it checks token expiration.

    If token passes a validation, returns
    a user instance corresponding with user_id stored
    in the incoming token.
    """
    try:
        data = jwt.decode(token, settings.SECRET_KEY, algorithms=[HS256_ALGORITHM])
    except jwt.DecodeError:
        raise NotAuthenticated("Invalid token")

    model_cls = get_user_model()

    try:
        user = model_cls.objects.get(pk=data["user_%s_id" % (scope)])
    except (model_cls.DoesNotExist, KeyError):
        raise NotAuthenticated("Invalid token")
    else:
        return user