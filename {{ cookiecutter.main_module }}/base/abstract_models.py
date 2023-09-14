# Standard Library
import uuid

from django.db import models
from django.utils import timezone


class UUIDModel(models.Model):
    """An abstract base class model that makes primary key `id` as UUID
    instead of default auto incremented number.
    """

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    class Meta:
        abstract = True

class AbstractBase(models.Model):
    """An abstract base class model that provides bunch of necessary options.
    Recommended to use with every model
    """
    id = models.BigAutoField(primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
