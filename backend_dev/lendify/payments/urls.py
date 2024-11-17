from django.urls import path
from .views import LoanInstallmentPaymentView, BankPersonnelPaymentsView, LoanCustomerPaymentsView

urlpatterns = [
    path('api/loan-customer/payments/pay-installment/', LoanInstallmentPaymentView.as_view(), name='pay_installment'),
    path('api/bank-personnel/payments/', BankPersonnelPaymentsView.as_view(), name='loan_provider_payments'),
    path('api/loan-customer/payments/', LoanCustomerPaymentsView.as_view(), name='loan_customer_payments'),
]
