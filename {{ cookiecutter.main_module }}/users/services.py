import string
import random
import logging

from django.conf import settings
from mail_templated import EmailMessage

from users.models import User
from users.exceptions import UnableToSendActivationEmail

logger = logging.getLogger(__name__)

class AuthServices:
    @staticmethod
    def send_account_activation_email(user: User, template_name):
        try:
            activation_url = f"{settings.DOMAIN}/api/activate?token={user.token}"
            ctx = {"activation_url": activation_url}
            message = EmailMessage(
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email],
                template_name=template_name,
                context=ctx,
            )
            message.send()
        except Exception as ex:
            logger.info(f"Unable to send account activation email to {user.email}. Error: {ex}")
            raise UnableToSendActivationEmail(
                f"Unable to send account activation email to {user.email}. Error: {ex}"
            )

    @staticmethod
    def create_user_account(
        phone_number=None,
        email=None,
        first_name=None,
        last_name=None,
        password=None,
        username=None,
    ) -> User:
        user = User.objects.create_user(email=email, phone_number=phone_number, first_name=first_name, last_name=last_name, username=username, password=password)
        return user

    @staticmethod    
    def generate_otp(length=6):
        """
        A util function which may be used in case of phone number verification and OTP based login
        """
        characters = string.digits
        otp = ''.join(random.choice(characters) for _ in range(length))
        return otp
