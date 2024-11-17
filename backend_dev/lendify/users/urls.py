from django.urls import path, include
from django.contrib.auth import views as auth_views
from users.views import CreateCustomerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import CustomTokenObtainPairView
urlpatterns = [
    path("api/user/register/", CreateCustomerView.as_view(), name="register new customer"),
    path("api/user/login/", CustomTokenObtainPairView.as_view(), name="get jwt tokens"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="refresh token"),
    path("api-auth/", include("rest_framework.urls"))

]
