from django.contrib import admin

from .models import Account, PaymentTransaction


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ["id", "email", "full_name", "created_at"]
    search_fields = ["email", "full_name"]


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "amount", "currency", "status", "idempotency_key", "created_at"]
    list_filter = ["status", "currency"]
    search_fields = ["idempotency_key"]
