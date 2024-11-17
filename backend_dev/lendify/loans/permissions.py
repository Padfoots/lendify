from rest_framework.permissions import BasePermission

class IsBankPersonnel(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'bank_personnel'


class IsLoanCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'loan_customer'
    

