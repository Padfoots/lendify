from django.db import models
from decimal import Decimal
class LoanPackage(models.Model):
    name = models.CharField(max_length=100)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    max_amount = models.DecimalField(max_digits=12, decimal_places=2)
    min_amount = models.DecimalField(max_digits=12, decimal_places=2)
    min_duration_months = models.PositiveIntegerField()
    max_duration_months = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.package_id})"
    

class LoanApplication(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('Active', 'Active'),
        ('REJECTED', 'Rejected'),
    ]

    customer = models.ForeignKey('users.LoanCustomer', on_delete=models.CASCADE)
    loan_package = models.ForeignKey('LoanPackage', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    term_months = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    applied_at = models.DateTimeField(auto_now_add=True)
    outstanding_balance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    installment_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Application #{self.id} by {self.customer} for {self.loan_package.name}"
    
    class Meta:
        permissions = [('can_add_loan_package', 'can add a loan package')]
