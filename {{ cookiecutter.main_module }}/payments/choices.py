# Payment status options
STARTED = "STARTED"
PENDING = "PENDING"
FAILED = "FAILED"
AUTHORIZED = "AUTHORIZED"
COLLECTED = "COLLECTED"
REFUNDED = "REFUNDED"
STATUS_CHOICES = (
    (STARTED, "Payment Transaction Started"),
    (PENDING, "Payment is pending"),
    (FAILED, "Payment failed"),
    (AUTHORIZED, "Payment Authorized"),
    (COLLECTED, "Payment collected"),
    (REFUNDED, "Refund Completed"),
)

# Payment gateway options
BANK_TRANSFER = "BANK_TRANSFER"
RAZORPAY = "RAZORPAY"
STRIPE = "STRIPE"
PAYPAL = "PAYPAL"
PHONEPE = "PHONEPE"
SERVICE_PROVIDER_CHOICES = (
    (BANK_TRANSFER, "Bank Transfer"),
    (RAZORPAY, "Razorpay"),
    (STRIPE, "Stripe"),
    (PAYPAL, "Paypal"),
    (PHONEPE, "Phonepe"),
)

# Payment type options
DEPOSIT = "DEPOSIT"  # Partial First Time Payment
REMAINING = "REMAINING"  # Remaining Payment after Deposit
UPFRONT = "UPFRONT"  # Full upfront payment
PAYMENT_TYPE_CHOICES = (
    (DEPOSIT, "Deposit"),
    (REMAINING, "Remaining"),
    (UPFRONT, "Upfront"),
)

# Refund reasons
REASON_OTHER = "Other"
REFUND_REASON_CHOICES = ((REASON_OTHER, "Other"),)
