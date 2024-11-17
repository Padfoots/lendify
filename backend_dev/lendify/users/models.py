from django.contrib.auth.models import AbstractUser
from django.db import models
from decimal import Decimal

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('bank_personnel', 'Bank Personnel'),
        ('loan_provider', 'Loan Provider'),
        ('loan_customer', 'Loan Customer'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class BankPersonnel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class LoanProvider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class LoanCustomer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    loan_balance = models.DecimalField(
    max_digits=10, 
    decimal_places=2, 
    default= Decimal('0.00'))

    def adjust_balance(self, amount):
        self.loan_balance += amount
        self.save()

    



