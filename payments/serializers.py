from rest_framework import serializers

from .models import PaymentTransaction, Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id", "email", "full_name", "created_at"]


class PaymentTransactionSerializer(serializers.ModelSerializer):
    user_email = serializers.SerializerMethodField()

    class Meta:
        model = PaymentTransaction
        fields = [
            "id",
            "user",
            "user_email",
            "amount",
            "currency",
            "status",
            "idempotency_key",
            "description",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "status", "created_at", "updated_at"]

    def get_user_email(self, obj):
        # BUG: causes N+1 — each payment triggers a separate query for user
        return obj.user.email


class CreatePaymentSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    currency = serializers.CharField(max_length=3, default="USD")
    idempotency_key = serializers.CharField(max_length=255, required=False, allow_null=True)
    description = serializers.CharField(required=False, default="")

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be positive.")
        return value

    def validate_user_id(self, value):
        if not Account.objects.filter(id=value).exists():
            raise serializers.ValidationError("Account not found.")
        return value
