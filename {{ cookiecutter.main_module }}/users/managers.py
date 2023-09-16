from django.contrib.auth.models import BaseUserManager

from base.managers import AllObjectsManager

class UserAllObjectsManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(
        self,
        email: str,
        phone_number: str,
        password: str,
        is_active: bool,
        is_staff: bool,
        is_superuser: bool,
        **extra_fields,
    ):
        user = self.model(
            email=email,
            phone_number=phone_number,
            is_active=is_active,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        
        from users.models import UserRole
        UserRole.objects.create(user=user)
        return user

    def create_user(self, email: str, phone_number: str, password=None, **extra_fields):
        """Creates and saves a User with the given email and password."""
        return self._create_user(email, phone_number, password, is_active=False, is_staff=False, is_superuser=False, **extra_fields)

    def create_superuser(self, email: str, password: str, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)

class UserRoleAllObjectsManager(AllObjectsManager):
    pass