import os

import requests
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.models import User
from users.tokens import account_activation_token


# REGISTRATION
class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True, max_length=50)
    types = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            types=validated_data["types"],
        )
        token = account_activation_token.make_token(user=user)
        user.token = token
        try:
            if self.validateEmail(validated_data["email"]):
                user.save()
                self.send_confirmation_email(user=user, token=token)
        except:
            raise ValidationError({"email": [_("User already exists")]})

        return user

    def send_confirmation_email(self, user, token):
        return requests.post(
            "https://api.eu.mailgun.net/v3/cleanstock.eu/messages",
            auth=("api", os.getenv("MAILGUN_API_KEY")),
            data={"from": "Clean Stock Team <noreply@cleanstock.eu>",
                  "to": user.email,
                  "subject": "Welcome to Clean Stock",
                  "template": "confirm_email",
                  "v:domain": "127.0.0.1:7000",
                  "v:uid": f"{urlsafe_base64_encode(force_bytes(user.pk))}",
                  "v:token": f"{token}",
                  }
        )

    def validateEmail(self, email):
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False


class RegistrationPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True, validators=[validate_password], max_length=128, min_length=6
    )
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True, validators=[validate_password], max_length=128, min_length=6
    )


# EMAIL VERIFICATION
class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


# CHANGE PASSWORD
class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('old_password', 'new_password', 'confirm_new_password')
