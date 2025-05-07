from django.urls import path
from .views import RegisterView, LogoutView, CustomTokenObtainPairView, verify_email, request_otp, login_with_otp


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-email/', verify_email),
    path('login/', CustomTokenObtainPairView.as_view()),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('request-otp/', request_otp, name='request-otp'),
    path('login-with-otp/', login_with_otp, name='login-with-otp'),
]