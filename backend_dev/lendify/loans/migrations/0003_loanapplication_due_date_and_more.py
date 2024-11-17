# Generated by Django 5.1.3 on 2024-11-16 19:11

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0002_alter_loanapplication_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='loanapplication',
            name='due_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='loanapplication',
            name='installment_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='loanapplication',
            name='outstanding_balance',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10),
        ),
    ]