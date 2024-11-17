from rest_framework import serializers
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import LoanCustomer, LoanProvider, BankPersonnel, Admin, User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomerRegistrationSerializer(serializers.ModelSerializer):
    user_type = serializers.ChoiceField(choices=[('loan_provider', 'Loan Provider'), ('loan_customer', 'Loan Customer')])
    
    class Meta:
        model = User
        fields = ["id", "username", "password", "email", "user_type"]
        extra_kwargs = {"password": {"write_only": True}}


    def create(self, validated_data):
        user = User.objects.create_user(
        username=validated_data['username'],
        password=validated_data['password'],
        email=validated_data['email'],
        user_type=validated_data['user_type']
        )

        user_type = validated_data.get('user_type')

        if user_type == 'loan_provider':
            LoanProvider.objects.create(
                user=user,

            )
        elif user_type == 'loan_customer':
            LoanCustomer.objects.create(
                user=user,
            )

        return user
    
class BankPersonnelRegistrationSerializer(serializers.ModelSerializer):
    user_type = serializers.ChoiceField(choices=[('bank_personnel', 'Bank Personnel')], default='bank_personnel')
    
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'user_type', 'contact_number']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user_type = validated_data.pop('user_type')
        contact_number = validated_data.pop('contact_number')

        # Create the user with the validated data
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            user_type=user_type
        )

        # Create BankPersonnel profile
        BankPersonnel.objects.create(
            user=user,
            contact_number=contact_number
        )

        return user
    

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['user_type'] = user.user_type  # Assuming user.user_type exists
        
        return token