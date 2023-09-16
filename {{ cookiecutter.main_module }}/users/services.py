from django.conf import settings
from mail_templated import EmailMessage

from users.models import User

class AuthServices:
    @staticmethod
    def send_account_activation_email(user: User, template_name):
        ctx = {"domain": settings.DOMAIN, "token": user.token}
        message = EmailMessage(
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
            template_name=template_name,
            context=ctx,
        )
        message.send()

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