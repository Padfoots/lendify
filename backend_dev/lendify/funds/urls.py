from django.urls import path
from .views import CreateFundApplicationView, CreateFundView, FundApplicationListView, FundApplicationActionView, LoanProviderFundApplicationsView

urlpatterns = [
    path('api/loan-provider/funds/apply/', CreateFundApplicationView.as_view(), name='create_fund_application'),
    path('api/loan-provider/funds/applications/', LoanProviderFundApplicationsView.as_view(), name='loan_provider_fund_applications'),
    
    path('api/bank-personnel/fund/update-limit/', CreateFundView.as_view(), name='update_fund_limit'),
    path('api/bank-personnel/funds/applications/<int:fund_application_id>/action/<str:action>/', FundApplicationActionView.as_view(), name='fund_application_action'),
    path('api/bank-personnel/funds/fund-applications/', FundApplicationListView.as_view(), name='fund_applications_list'),


]
