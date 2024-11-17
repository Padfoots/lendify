from rest_framework.permissions import BasePermission

class IsLoanProvider(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'loan_provider'
    

class IsBankPersonnel(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'bank_personnel'