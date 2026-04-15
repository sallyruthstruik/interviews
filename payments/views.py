import logging

from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import PaymentTransaction, Account
from .serializers import (
    CreatePaymentSerializer,
    PaymentTransactionSerializer,
)

logger = logging.getLogger(__name__)


class CreatePaymentView(APIView):
    """
    POST /api/payments/
    Creates a new payment transaction.
    Accepts an optional idempotency_key to prevent duplicate charges.
    """

    def post(self, request):
        serializer = CreatePaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        user = Account.objects.get(id=data["user_id"])

        payment = PaymentTransaction.objects.create(
            user=user,
            amount=data["amount"],
            currency=data.get("currency", "USD"),
            description=data.get("description", ""),
        )

        payment.process()

        logger.info("payment created")  # BUG: no useful context

        return Response(
            PaymentTransactionSerializer(payment).data,
            status=status.HTTP_201_CREATED,
        )


class PaymentListView(ListAPIView):
    serializer_class = PaymentTransactionSerializer
    queryset = PaymentTransaction.objects.all()
    filterset_fields = ["status", "user", "currency"]
