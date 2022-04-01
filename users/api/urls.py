from django.urls import path, re_path
from users.api.views import (
    RegistrationView,
    ChangePasswordView,
    RegistrationPasswordView,
    VerifyEmailView,
)

app_name = "users"

urlpatterns = [
    path('register/', RegistrationView.as_view(), name="register"),
    path('registration_password/<str:uidb64>/<str:token>/',
         RegistrationPasswordView.as_view(), name="registration_password"),
    path('verify_email/', VerifyEmailView.as_view(), name="verify_email"),
    path('change_password/', ChangePasswordView.as_view(), name="change_password"),
]
