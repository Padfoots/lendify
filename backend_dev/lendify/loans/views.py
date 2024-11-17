from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import LoanPackage
from .serializers import LoanPackageSerializer, LoanApplicationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import LoanPackage
from .serializers import LoanPackageSerializer, GetLoanPackagesSerializer, GetLoanApplicationSerializer
from .permissions import IsBankPersonnel, IsLoanCustomer
from django.shortcuts import get_object_or_404
from .utils.redis_client import get_redis_client
from .models import LoanPackage, LoanApplication
import json
from decimal import Decimal
from users.models import LoanCustomer
from funds.models import Fund
from datetime import datetime, timedelta
from django.db import transaction
from drf_spectacular.utils import extend_schema

# endpoint for BankPersonnel to create a new Loan Package
class LoanPackageCreateView(generics.CreateAPIView):
    queryset = LoanPackage.objects.all()
    serializer_class = LoanPackageSerializer
    permission_classes = [permissions.IsAuthenticated]
    @extend_schema(responses=LoanPackageSerializer)
    def perform_create(self, serializer):
        if not self.request.user.user_type == "bank_personnel":
            raise PermissionDenied("You do not have permission to add a loan package.")
        serializer.save()


# endpoint for BankPersonnel to perform crud operation on a Loan Package
class LoanPackageDetailView(APIView):

    permission_classes = [IsBankPersonnel]

    @extend_schema(responses=LoanPackageSerializer)
    def get(self, request, pk):
        loan_package = get_object_or_404(LoanPackage, pk=pk)
        serializer = LoanPackageSerializer(loan_package)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @extend_schema(responses=LoanPackageSerializer)    
    def put(self, request, pk):

        loan_package = get_object_or_404(LoanPackage, pk=pk)
        serializer = LoanPackageSerializer(loan_package, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        loan_package = get_object_or_404(LoanPackage, pk=pk)
        loan_package.delete()
        return Response({"message": "Loan Package deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


# endpoint for any authenticated user to fetch the list of Loan Packages available
class LoanPackageListView(APIView):
    @extend_schema(responses=GetLoanPackagesSerializer)
    def get(self, request):
        loan_packages = LoanPackage.objects.all()
        serializer = GetLoanPackagesSerializer(loan_packages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

# endpoint for LoanCustomer to apply for a new Loan application
class LoanApplicationView(APIView):
    permission_classes = [IsLoanCustomer]
    @extend_schema(responses=LoanApplicationSerializer)
    def post(self, request):
        user = request.user
        
        # Get the LoanCustomer instance
        loan_customer = get_object_or_404(LoanCustomer, user=user)

        # Validate loan package
        loan_package_id = request.data.get('loan_package')
        
        loan_package = get_object_or_404(LoanPackage, id=loan_package_id)
        term_months = request.data.get('term_months')


        # Validate amount
        amount = request.data.get('amount')
        if not amount or Decimal(amount) <= 0:
            return Response({"error": "Invalid loan amount."}, status=status.HTTP_400_BAD_REQUEST)
        if amount < loan_package.min_amount or amount > loan_package.max_amount:
            return Response({"error": "Amount is outside of package limits."}, status=status.HTTP_400_BAD_REQUEST)
        
        if term_months < loan_package.min_duration_months or term_months > loan_package.max_duration_months:
            return Response({"error": "Loan Term is outside of package limits."}, status=status.HTTP_400_BAD_REQUEST)
        # Create loan application
        loan_application = LoanApplication.objects.create(
            customer=loan_customer,
            loan_package=loan_package,
            amount=Decimal(amount),
            term_months=term_months
        )
        # Serialize and return response
        serializer = LoanApplicationSerializer(loan_application)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



# endpoint for loancustomer to get his loan applications
class LoanApplicationListView(APIView):
    permission_classes = [IsLoanCustomer]
    @extend_schema(responses=GetLoanApplicationSerializer)
    def get(self, request):

        user = request.user
        
        # Ensure that the user is a LoanCustomer
        loan_customer = get_object_or_404(LoanCustomer, user=user)

        
        # Fetch all loan applications for this LoanCustomer
        loan_applications = LoanApplication.objects.filter(customer=loan_customer)
        
        # Serialize the loan applications data
        serializer = GetLoanApplicationSerializer(loan_applications, many=True)
        
        # Return the loan applications data as a JSON response
        return Response({'loan_applications': serializer.data}, status=status.HTTP_200_OK)



#endpoint for BankPersonnel to approve/reject a loan
class LoanApplicationActionView(APIView):
    permission_classes = [IsBankPersonnel] 

    @extend_schema(responses=GetLoanApplicationSerializer)
    def post(self, request, loan_application_id, action):
        if action not in ["accept", "reject"]:
            return Response({"detail": "Invalid action. Choose either 'accept' or 'reject'."},
                            status=status.HTTP_400_BAD_REQUEST)


        # Fetch the loan application
        loan_application = get_object_or_404(LoanApplication, id=loan_application_id)
        loan_customer = get_object_or_404(LoanCustomer, user=loan_application.customer.user)




        # first check that the application is not active

        if loan_application.status == "active": 
            return Response({"detail": "Invalid action. the loan has been already activated."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Update the loan application status based on the action
        fund = Fund.objects.first()
        if action == "accept":
            if not fund.has_sufficient_funds(loan_application.amount):
                return Response({"detail": "Invalid action. Not Enough funds to accept the Loan."},
                            status=status.HTTP_400_BAD_REQUEST)
            with transaction.atomic():

                loan_amount = loan_application.amount
                term_months = loan_application.term_months
                interest_rate = loan_application.loan_package.interest_rate 
                monthly_interest_rate = interest_rate /100 /12
                
                fund.adjust_funds(-loan_application.amount)
                loan_customer.adjust_balance(loan_application.amount)

                installment_amount = (loan_amount * monthly_interest_rate * (1 + monthly_interest_rate)**term_months) / \
                ((1 + monthly_interest_rate)**term_months - 1)

                
                #todo: set the outstanding balance
                total_payment = installment_amount * term_months
                

                loan_application.outstanding_balance = total_payment
                
                #todo: set the installement amount
                installment_amount = total_payment / term_months
                loan_application.installment_amount = installment_amount
                
                #todo: set the due date
                first_due_date = (datetime.now() + timedelta(days=30) ).date()
                loan_application.due_date = first_due_date
                loan_application.status = "active"
                loan_application.save()
                loan_customer.save()
        elif action == "reject":
            loan_application.status = "rejected"
            loan_application.save()

        # Save the updated loan application




        # Serialize and return the updated loan application data
        serializer = GetLoanApplicationSerializer(loan_application)

        return Response({'loan_application': serializer.data}, status=status.HTTP_200_OK)


#endpoint for BankPersonnel to get a list of all loan applications
class LoanApplicationListForBankPersonnel(APIView):
    """
    Endpoint for BankPersonnel to get a list of all loan applications.
    """

    permission_classes = [IsBankPersonnel]

    @extend_schema(responses=GetLoanApplicationSerializer)
    def get(self, request):
        # Retrieve all LoanApplications
        loan_applications = LoanApplication.objects.all()
        
        # Serialize the data
        serializer = GetLoanApplicationSerializer(loan_applications, many=True)
        
        # Return the loan applications data as a JSON response
        return Response({'loan_applications': serializer.data}, status=status.HTTP_200_OK)





