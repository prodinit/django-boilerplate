from typing import List

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.functional import cached_property
from django.forms.models import model_to_dict
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save

from base.abstract_models import AbstractBase
from users.choices import COUNTRY_CHOICES, GENDER_CHOICES, AUTH_PROVIDER, EMAIL
from users.managers import UserAllObjectsManager, UserRoleAllObjectsManager


class User(AbstractUser, AbstractBase):
    # We dont need date_joined from AbstractUser model as we have built our custom AbstractBase model with created_at and updated_at fields
    date_joined = None

    first_name: str = models.CharField(max_length=50, blank=True, null=True)
    last_name: str = models.CharField(max_length=50, blank=True, null=True)
    username: str = models.CharField(max_length=200, blank=True, null=True)
    email: str = models.EmailField(unique=True)
    is_email_verified: bool = models.BooleanField(default=False)
    phone_number: str = models.CharField(
        max_length=16,
        unique=True,
        blank=True,
        null=True,
    )
    is_phone_number_verified: bool = models.BooleanField(default=False)
    is_active: bool = models.BooleanField(
        default=False,
    )
    is_staff: bool = models.BooleanField(
        default=False,
    )
    is_superuser: bool = models.BooleanField(
        default=False,
    )
    address: str = models.TextField(
        blank=True,
        null=True,
    )
    city: str = models.CharField(
        max_length=31,
        blank=True,
        null=True,
    )
    state: str = models.CharField(
        max_length=31,
        blank=True,
        null=True,
    )
    postal_code: str = models.CharField(
        blank=True,
        null=True,
        max_length=12,
    )
    country: str = models.CharField(
        blank=True, null=True, max_length=2, choices=COUNTRY_CHOICES
    )
    gender: str = models.CharField(
        choices=GENDER_CHOICES,
        blank=True,
        null=True,
        max_length=22,
    )
    auth_provider = models.CharField(
        choices=AUTH_PROVIDER,
        default=EMAIL,
        max_length=50,
    )

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserAllObjectsManager()

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.id}"

    @cached_property
    def all_roles(self) -> List[str]:
        """
        This wil query all assigned roles for current user
        and set that to self.user_roles attribute
        @return: Queryset list
        Warning: don't make function call ()
        self.all_roles will return the response
        @return: list
        """
        user_roles = UserRole.objects.filter(user_id=self.id).values_list(
            "role", flat=True
        )
        return list(user_roles)

    def has_role(self, role) -> bool:
        """
        Check if current user has requested role
        @param role: string
        @return: boolean
        """
        user_roles = self.all_roles
        return role in user_roles

    @property
    def role(self):
        """
        Get role of currect user
        """
        return list(
            UserRole.objects.filter(user_id=self.id).values_list("role", flat=True)
        )

    @property
    def token(self):
        """
        Get token of current user
        """
        return Token.objects.get(user_id=self.id).key

    def run_validators(self) -> None:
        for field_name, field_value in model_to_dict(self).items():
            model_field = getattr(User, field_name)
            field = getattr(model_field, "field", object())
            validators = getattr(field, "validators", list())
            for validator_func in validators:
                if field_value is not None:
                    validator_func(field_value)

    def save(self, *args, **kwargs):
        self.run_validators()
        return super().save(*args, **kwargs)


# method for create token of user
@receiver(post_save, sender=User, dispatch_uid="create_token")
def create_token(sender, instance, **kwargs):
    Token.objects.get_or_create(user=instance)


class UserRole(AbstractBase):
    user: User = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    ADMIN = "ADMIN"
    USER = "User"
    ROLE_CHOICES = ((ADMIN, "Admin"), (USER, "User"))
    role: str = models.CharField(
        choices=ROLE_CHOICES,
        default=USER,
        max_length=16,
    )

    objects = UserRoleAllObjectsManager()

    def __str__(self):
        return f"User: {self.user_id} UserRole: {self.role}"

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)
