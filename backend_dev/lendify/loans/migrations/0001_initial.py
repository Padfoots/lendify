# Generated by Django 5.1.3 on 2024-11-16 10:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0002_remove_loancustomer_contact_number_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoanPackage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('interest_rate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('max_amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('min_amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('min_duration_months', models.PositiveIntegerField()),
                ('max_duration_months', models.PositiveIntegerField()),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='LoanApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('term_months', models.PositiveIntegerField()),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected')], default='PENDING', max_length=10)),
                ('applied_at', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.loancustomer')),
                ('loan_package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loans.loanpackage')),
            ],
            options={
                'permissions': [('can_add_loan_package', 'can add a loan package')],
            },
        ),
    ]
