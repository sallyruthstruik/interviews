import uuid
import logging

from django.db import models

logger = logging.getLogger(__name__)


class Account(models.Model):
    """Simplified account model for the payment system."""

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.email


class PaymentTransaction(models.Model):
    """
    Payment transactions, extremely huge table (1MM rows)
    """
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        SUCCESS = "success", "Success"
        FAILED = "failed", "Failed"

    class Type(models.TextChoices):
        DEPOSIT = "deposit", "Deposit"
        WITHDRAW = "withdraw", "Withdraw"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="payments")
    type = models.CharField(
        max_length=10,
        choices=Type.choices,
        default=Type.DEPOSIT,
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default="USD")
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
    )
    idempotency_key = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "payment_transactions"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Payment {self.id} — {self.amount} {self.currency} [{self.status}]"

    def process(self):
        """Simulate payment processing."""
        import random
        import time

        logger.info("processing payment")

        time.sleep(random.uniform(0.1, 0.3))

        if random.random() < 0.85:
            self.status = self.Status.SUCCESS
        else:
            self.status = self.Status.FAILED

        self.save()
        logger.info("payment done")
