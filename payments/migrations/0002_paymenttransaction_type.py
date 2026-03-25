from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payments", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="paymenttransaction",
            name="type",
            field=models.CharField(
                choices=[("deposit", "Deposit"), ("withdraw", "Withdraw")],
                default="deposit",
                max_length=10,
            ),
        ),
    ]
