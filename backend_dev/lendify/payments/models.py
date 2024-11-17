from django.db import models
from decimal import Decimal
from django.conf import settings



class LoanPayment(models.Model):
    loan_application = models.ForeignKey('loans.LoanApplication', on_delete=models.CASCADE, related_name='payments')
    customer = models.ForeignKey('users.LoanCustomer', on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)