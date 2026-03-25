import logging

from celery import shared_task

from .models import PaymentTransaction

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=5)
def process_payment(self, payment_id: str):
    try:
        payment = PaymentTransaction.objects.get(pk=payment_id)
    except PaymentTransaction.DoesNotExist:
        logger.error("Payment %s not found, skipping", payment_id)
        return

    if payment.status != PaymentTransaction.Status.PENDING:
        logger.info("Payment %s already processed (status=%s), skipping", payment_id, payment.status)
        return

    payment.process()
    logger.info("Payment %s processed, status=%s", payment_id, payment.status)
