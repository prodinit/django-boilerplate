import jsonfield
import uuid
from math import ceil

from django.db import models
from django.utils import timezone
from django.conf import settings

from base.abstract_models import AbstractBase
from users.models import User
from payments.utils import get_all_currencies_code
from payments.constants import Constants
from payments.managers import PaymentTransactionAllObjectsManager
from payments.choices import (
    STARTED,
    STATUS_CHOICES,
    SERVICE_PROVIDER_CHOICES,
    PAYMENT_TYPE_CHOICES,
    UPFRONT,
    REFUND_REASON_CHOICES,
)


# Create your models here.
class PaymentTransaction(AbstractBase):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    currency = models.CharField(
        max_length=3, choices=get_all_currencies_code(), default=Constants.INR
    )
    usd_conversion_rate = models.DecimalField(
        decimal_places=5, max_digits=10, default=0.012
    )

    checkout_token = models.CharField(max_length=50, blank=True, null=True)
    amount = models.PositiveIntegerField()
    order_callback_data = jsonfield.JSONField()
    charge_callback_data = jsonfield.JSONField()
    capture_callback_data = jsonfield.JSONField(blank=True, null=True)
    order_id = models.CharField(max_length=20, unique=True)
    charge_id = models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )

    status = models.CharField(
        choices=STATUS_CHOICES,
        default=STARTED,
        max_length=11,
    )

    service_provider = models.CharField(
        choices=SERVICE_PROVIDER_CHOICES,
        default=None,
        max_length=20,
        blank=True,
        null=True,
    )
    is_manual = models.BooleanField(default=False)
    is_refund = models.BooleanField(default=False)
    transaction_date = models.DateTimeField(default=timezone.now)

    payment_type = models.CharField(
        choices=PAYMENT_TYPE_CHOICES,
        default=UPFRONT,
        max_length=20,
    )

    refund_reason = models.CharField(
        choices=REFUND_REASON_CHOICES,
        default=None,
        blank=True,
        null=True,
        max_length=20,
    )

    razorpay_signature = models.CharField(max_length=100, blank=True, null=True)
    amount_in_inr = models.PositiveIntegerField(default=None, blank=True, null=True)
    amount_in_usd = models.PositiveIntegerField(default=None, blank=True, null=True)

    all_objects = PaymentTransactionAllObjectsManager()

    def __str__(self):
        return f"{self.id} {self.order_id} {self.status}"

    @staticmethod
    def generate_order_id():
        max_length = settings.ORDER_ID_MAX_LENGTH
        return "".join([uuid.uuid4().hex for _ in range(ceil(max_length / 32))])[
            :max_length
        ]

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)
