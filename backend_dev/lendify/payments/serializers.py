from rest_framework import serializers
from .models import LoanPayment

class LoanPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanPayment
        fields = ['loan_application', 'amount_paid']


class LoanPaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanPayment
        fields = '__all__'

