from django.db import models
from decimal import Decimal
from users.models import LoanProvider
class Fund(models.Model):
    total_available_funds = models.DecimalField(
        max_digits=20, decimal_places=2, default=Decimal('0.00')
    )

    funding_limit = models.DecimalField(
        max_digits=20, decimal_places=2, default=Decimal('1000000.00')  # Example limit, adjust as needed
    )

    def __str__(self):
        return f"Total Available Funds: {self.total_available_funds}"
    
    def exceeds_funding_limit(self, amount):
        return self.total_available_funds + amount > self.funding_limit

    # Method to add or subtract funds
    def adjust_funds(self, amount):
        self.total_available_funds += amount
        self.save()

    # Ensures funds cannot go negative
    def has_sufficient_funds(self, amount):
        return self.total_available_funds >= amount
    
class FundApplication(models.Model):
    # Reference to the user who applied for the fund
    LoanProvider = models.ForeignKey(LoanProvider, on_delete=models.CASCADE)
    
    # The amount requested
    amount_requested = models.DecimalField(max_digits=20, decimal_places=2)
    
    # Status of the application (pending, approved, rejected)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('active', 'Active'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
    # Date when the application was created
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Date when the application was updated
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Application by {self.user.username} for {self.amount_requested}"

    def can_approve(self):
        fund = Fund.objects.first()
        if fund.has_sufficient_funds(self.amount_requested) and not fund.exceeds_funding_limit(self.amount_requested):
            return True
        return False

    # Approve the application (deduct funds and update the status)
    def approve(self):
        if self.can_approve():
            fund = Fund.objects.first()
            fund.adjust_funds(-self.amount_requested)
            self.status = 'approved'
            self.save()
        else:
            raise ValueError("Insufficient funds to approve the application.")

    def reject(self):
        self.status = 'rejected'
        self.save()

