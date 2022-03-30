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
    re_path('registration_password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
            RegistrationPasswordView.as_view(), name="registration_password"),
    path('verify_email/', VerifyEmailView.as_view(), name="verify_email"),
    path('change_password/', ChangePasswordView.as_view(), name="change_password"),
]
