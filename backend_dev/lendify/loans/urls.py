from django.urls import path
from .views import LoanPackageCreateView, LoanPackageListView, LoanPackageDetailView, LoanApplicationActionView
from .views import LoanApplicationView, LoanApplicationListView, LoanApplicationListForBankPersonnel
urlpatterns = [
    
    path('api/bank-personnel/loans/add/loan-package/', LoanPackageCreateView.as_view(), name='create-loan-package'),
    path('api/bank-personnel/loans/loan-applications/', LoanApplicationListForBankPersonnel.as_view(), name='loan_applications_for_bank_personnel'),
    path('api/bank-personnel/loans/application/<int:loan_application_id>/action/<str:action>/', LoanApplicationActionView.as_view(), name='update-loan-application-status'),
    path('api/bank-personnel/loans/loan-packages/<int:pk>/', LoanPackageDetailView.as_view(), name='loan-package-detail'),
    
    path('api/loan-customer/loan-packages/', LoanPackageListView.as_view(), name='get all loan-packages'),
    path('api/loan-customer/loans/applications/apply/', LoanApplicationView.as_view(), name='loan-apply'),
    path('api/loan-customer/loans/applications/', LoanApplicationListView.as_view(), name='get_loan_applications'),




]
