from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from decimal import Decimal
from .models import LoanPayment
from loans.models import LoanApplication
from .permissions import IsLoanCustomer, IsBankPersonnel
from .serializers import LoanPaymentsSerializer
from users.models import LoanCustomer


class LoanInstallmentPaymentView(APIView):
    permission_classes = [IsLoanCustomer]

    def post(self, request):
        # Get data from the request
        loan_application_id = request.data.get("loan_application_id")
        amount = request.data.get("amount")
        user = request.user
        loan_customer = get_object_or_404(LoanCustomer, user=user)

        if not loan_application_id or not amount:
            return Response({"detail": "Loan application ID and payment amount are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            amount = Decimal(amount)
            if amount <= 0:
                raise ValueError
        except ValueError:
            return Response({"detail": "Invalid payment amount."}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the loan application
        loan_application = get_object_or_404(LoanApplication, id=loan_application_id, customer=loan_customer)

        # Validate payment
        if loan_application.status != "active":
            return Response({"detail": "Payments can only be made for accepted loans."}, status=status.HTTP_400_BAD_REQUEST)

        if amount > loan_application.outstanding_balance:
            return Response({"detail": "Payment amount exceeds the outstanding balance."}, status=status.HTTP_400_BAD_REQUEST)

        if amount < loan_application.installment_amount:
            return Response({"detail": "amount is less than the loan installement."}, status=status.HTTP_400_BAD_REQUEST)

        # Process payment
        loan_application.outstanding_balance -= amount
        loan_application.save()

        # Create payment record
        LoanPayment.objects.create(
            loan_application=loan_application,
            customer=request.user.loancustomer,
            amount_paid=amount
        )

        return Response({"detail": "Payment successful.", "outstanding_balance": loan_application.outstanding_balance},
                        status=status.HTTP_200_OK)


#todo: create an endpoint for bankpersonnel to get all payments
class BankPersonnelPaymentsView(APIView):
    permission_classes = [IsBankPersonnel]

    def get(self, request):
        # Fetch all payments made to LoanProviders
        payments = LoanPayment.objects.all()  # You can add filters if needed, e.g., by loan provider
        
        # Serialize the payment data
        serializer = LoanPaymentsSerializer(payments, many=True)
        
        return Response({"payments": serializer.data}, status=status.HTTP_200_OK)

#todo: create an endpoint for LoanCustomer to get his payments
class LoanCustomerPaymentsView(APIView):
    permission_classes = [IsLoanCustomer]

    def get(self, request):
        # Fetch payments related to the authenticated LoanCustomer
        user = request.user
        loan_customer = get_object_or_404(LoanCustomer, user=user)

        payments = LoanPayment.objects.filter(customer=loan_customer)
        
        # Serialize the payment data
        serializer = LoanPaymentsSerializer(payments, many=True)
        
        return Response({"payments": serializer.data}, status=status.HTTP_200_OK)