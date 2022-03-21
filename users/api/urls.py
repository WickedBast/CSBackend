from django.urls import path
from users.api.views import (
    RegistrationView,
    ChangePasswordView,
    RegistrationPasswordView,
    VerifyEmailView,
)

app_name = "users"

urlpatterns = [
    path('register/', RegistrationView.as_view(), name="register"),
    path('registration_password/', RegistrationPasswordView.as_view(), name="registration_password"),
    path('verify_email/', VerifyEmailView.as_view(), name="verify_email"),
    path('change_password/', ChangePasswordView.as_view(), name="change_password"),
]
