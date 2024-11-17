from rest_framework import serializers
from .models import FundApplication, Fund

# serializer for applying for a new fund application by LoanProvider
class CreateFundApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FundApplication
        fields = ['amount_requested']


class FundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fund
        fields = ['funding_limit']
    def validate_funding_limit(self, value):
        if value < 0:
            raise serializers.ValidationError("Funding limit cannot be negative.")
        return value
    

class FundApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FundApplication
        fields = '__all__'