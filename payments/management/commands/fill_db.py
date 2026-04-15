import random
import uuid

from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import BaseCommand

from payments.models import Account, PaymentTransaction


class Command(BaseCommand):
    help = "Seed database with sample users and payments"

    def add_arguments(self, parser):
        parser.add_argument(
            "--silent", action="store_true", help="Suppress output"
        )

    def handle(self, *args, **options):
        if PaymentTransaction.objects.count() > 0:
            return

        # Create admin
        user, _ = User.objects.get_or_create(
            username='admin',
            defaults=dict(
                is_superuser=True,
                is_staff=True,
                email='admin@test.com',
            )
        )
        user.set_password('123')
        user.save()

        silent = options["silent"]

        users_data = [
            {"email": "alice@example.com", "full_name": "Alice Johnson"},
            {"email": "bob@example.com", "full_name": "Bob Smith"},
            {"email": "charlie@example.com", "full_name": "Charlie Brown"},
        ]

        users = []
        for data in users_data:
            user = Account.objects.create(**data)
            users.append(user)
            if not silent:
                self.stdout.write(f"  Created user: {user.email}")

        statuses = [
            PaymentTransaction.Status.SUCCESS,
            PaymentTransaction.Status.SUCCESS,
            PaymentTransaction.Status.SUCCESS,
            PaymentTransaction.Status.PENDING,
            PaymentTransaction.Status.FAILED,
        ]

        for i in range(25):
            PaymentTransaction.objects.create(
                user=random.choice(users),
                amount=round(random.uniform(5.00, 500.00), 2),
                currency=random.choice(["USD", "EUR", "GBP"]),
                status=random.choice(statuses),
                idempotency_key=str(uuid.uuid4()) if random.random() > 0.3 else None,
                description=f"Payment #{i + 1}",
            )
