from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import FundApplication, Fund
from .serializers import CreateFundApplicationSerializer, FundSerializer, FundApplicationSerializer
from .permissions import IsLoanProvider, IsBankPersonnel
from decimal import Decimal
from users.models import LoanProvider
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema

# view for LoanProvider to apply for a LoanFund application
class CreateFundApplicationView(APIView):
    permission_classes = [IsLoanProvider]

    def post(self, request):
        user = request.user  

                # Get the LoanCustomer instance
        loan_provider = get_object_or_404(LoanProvider, user=user)

        # Validate the input data (amount_requested is required)
        amount_requested = request.data.get('amount_requested')

        if not amount_requested:
            return Response({"detail": "Amount requested is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            amount_requested = Decimal(amount_requested)  # Ensure it's a valid float
        except ValueError:
            return Response({"detail": "Invalid amount requested."}, status=status.HTTP_400_BAD_REQUEST)

        if amount_requested <= 0:
            return Response({"detail": "Amount requested must be greater than zero."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the requested amount exceeds the available funds
        fund = Fund.objects.first()  
        if not fund.exceeds_funding_limit(amount_requested):
            # Create the FundApplication instance
            fund_application = FundApplication.objects.create(
                LoanProvider=loan_provider,
                amount_requested=amount_requested,
                status='pending'  
            )

            serializer = CreateFundApplicationSerializer(fund_application)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response({
            "detail": "Insufficient funds or requested amount exceeds funding limit."
        }, status=status.HTTP_400_BAD_REQUEST)


# view for BankPersonnel to post and edit the the fund limit
class CreateFundView(APIView):
    permission_classes = [IsBankPersonnel]
    @extend_schema(responses=FundSerializer)
    def post(self, request):
        # Deserialize the request data
        serializer = FundSerializer(data=request.data)
        if serializer.is_valid():
            # Check if a Fund instance already exists
            if Fund.objects.exists():
                return Response(
                    {"detail": "A fund already exists. You cannot create another fund."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Save the new fund instance
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # Handle invalid input
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @extend_schema(responses=FundSerializer)
    def patch(self, request):
        try:
            # Fetch the existing fund
            fund = Fund.objects.first()
            if not fund:
                return Response({"detail": "Fund does not exist."}, status=status.HTTP_404_NOT_FOUND)

            # Deserialize and validate the incoming data
            serializer = FundSerializer(fund, data=request.data, partial=True)
            if serializer.is_valid():
                # Save the updated fund limit
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

# create a view for BankPersonnel to get all the loan fund applications
class FundApplicationListView(APIView):
    permission_classes = [IsBankPersonnel]
    @extend_schema(responses=FundApplicationSerializer)
    def get(self, request):
        try:
            fund_applications = FundApplication.objects.all()
            serializer = FundApplicationSerializer(fund_applications, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


# create a view for Bank Personnel to accept/ reject a loan fund application
class FundApplicationActionView(APIView):
    permission_classes = [IsBankPersonnel]
    @extend_schema(responses=FundApplicationSerializer)
    def post(self, request, fund_application_id, action):
        if not fund_application_id or not action:
            return Response(
                {"detail": "Fund application ID and action (accept/reject) are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if action not in ["accept", "reject"]:
            return Response(
                {"detail": "Invalid action. Choose either 'accept' or 'reject'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Fetch the fund application
        fund_application = get_object_or_404(FundApplication, id=fund_application_id)

        fund = Fund.objects.first()  

        if fund_application.status == "active":
            return Response(
                {"detail": "Invalid action. application is already been activated."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if action == "accept" and not fund.exceeds_funding_limit(fund_application.amount_requested) :
            fund.adjust_funds(fund_application.amount_requested)
            fund_application.status = "active"
            fund_application.save()

        elif action == "reject":
            fund_application.status = "rejected"
            fund_application.save()

        # Serialize and return the updated fund application
        serializer = FundApplicationSerializer(fund_application)
        return Response({'fund_application': serializer.data}, status=status.HTTP_200_OK)
    

# create an endpoint for LoanProvider to get their fund applications

class LoanProviderFundApplicationsView(APIView):
    permission_classes = [IsLoanProvider]
    @extend_schema(responses=FundApplicationSerializer)
    def get(self, request):
        # Get the LoanProvider object
        loan_provider = get_object_or_404(LoanProvider, user=request.user)

        # Fetch all fund applications for the loan provider
        fund_applications = FundApplication.objects.filter(LoanProvider_id=loan_provider)

        # Serialize the data
        serializer = FundApplicationSerializer(fund_applications, many=True)

        return Response({'fund_applications': serializer.data}, status=status.HTTP_200_OK)
    




