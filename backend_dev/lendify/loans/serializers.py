from rest_framework import serializers
from .models import LoanPackage, LoanApplication
from users.models import LoanCustomer  # Adjust import path as necessary

# serializer when creating a new LoanPackage
class LoanPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanPackage
        fields = [
            'name',
            'interest_rate',
            'max_amount',
            'min_amount',
            'min_duration_months',
            'max_duration_months',
            'description'
        ]


# Serializer to get all informations of Loan Package
class GetLoanPackagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanPackage
        fields = '__all__'

# Serializer to Register a new Loan Application
class LoanApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanApplication
        fields = ['loan_package', 'amount', 'term_months']


# Serializer to 
class GetLoanApplicationSerializer(serializers.ModelSerializer):
    loan_package = serializers.CharField(source='loan_package.name')  # Assuming LoanPackage has a `name` field
    
    class Meta:
        model = LoanApplication
        fields = '__all__'