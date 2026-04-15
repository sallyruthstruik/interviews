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
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "payment_transactions"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Payment {self.id} — {self.amount} {self.currency} [{self.status}]"

    def process(self):
        from .partner import PartnerClient

        logger.info("processing payment %s", self.id)

        client = PartnerClient()
        foreign_id = str(self.id)

        try:
            if self.type == self.Type.DEPOSIT:
                response = client.deposit(self.amount, self.currency, foreign_id)
            else:
                response = client.withdraw(self.amount, self.currency, foreign_id)

            self.status = (
                self.Status.SUCCESS if response.status == "success" else self.Status.FAILED
            )
        except Exception:
            logger.exception("partner call failed for payment %s", self.id)
            self.status = self.Status.FAILED

        self.save()
        logger.info("payment %s finished with status %s", self.id, self.status)
