import logging

from rest_framework import status
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

        idempotency_key = data.get("idempotency_key")
        if idempotency_key:
            existing = PaymentTransaction.objects.filter(
                idempotency_key=idempotency_key,
                user=user,
            ).first()
            if existing:
                logger.info("duplicate request")
                return Response(
                    PaymentTransactionSerializer(existing).data,
                    status=status.HTTP_200_OK,
                )

        payment = PaymentTransaction.objects.create(
            user=user,
            amount=data["amount"],
            currency=data.get("currency", "USD"),
            idempotency_key=idempotency_key,
            description=data.get("description", ""),
        )

        payment.process()

        logger.info("payment created")  # BUG: no useful context

        return Response(
            PaymentTransactionSerializer(payment).data,
            status=status.HTTP_201_CREATED,
        )
