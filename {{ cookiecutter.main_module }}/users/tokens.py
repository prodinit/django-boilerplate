import jwt 

from django.conf import settings

HS256_ALGORITHM = "HS256"


def get_token_for_user(user, scope: str) -> str:
    """Generate a new signed token containing a specified user limited for a scope (identified as a string)."""
    data = {"user_%s_id" % (scope): str(user.id)}
    return jwt.encode(data, settings.SECRET_KEY, algorithm=HS256_ALGORITHM)
