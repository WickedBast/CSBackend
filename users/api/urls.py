from django.urls import path
from users.api.views import (
    registration_view,
    ObtainAuthTokenView,
    ChangePasswordView,
    does_account_exist_view,
)

app_name = "users"

urlpatterns = [
    path('register', registration_view, name="register"),
    path('login', ObtainAuthTokenView.as_view(), name="login"),
    path('check_if_account_exists/', does_account_exist_view, name="check_if_account_exists"),
    path('change_password/', ChangePasswordView.as_view(), name="change_password"),
]
