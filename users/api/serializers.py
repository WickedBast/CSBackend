from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from django.utils.translation import gettext as _
from django.contrib.auth.password_validation import validate_password

from members.api.serializers import (
    IndividualMemberCreationSerializer,
    CompanyMemberCreationSerializer,
)
from partner.api.serializers import (
    PartnerCreationSerializer
)

from users.models import User
from django.contrib import auth


# REGISTRATION
class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=50)
    types = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            types=validated_data["types"],
        )
        try:
            if self.validate_email(validated_data["email"]) is not None:
                user.save()
                if user.types == "Individual" or "Company":
                    user.member = self.save_type()
                elif user.types == "Partner":
                    user.partner = self.save_type()
        except:
            raise ValidationError({"email": [_("User already exists")]})

        return user

    def validate_email(self, email):
        account = None
        try:
            account = User.objects.get(email=email)
        except User.DoesNotExist:
            return None
        if account is not None:
            return email

    def save_type(self):
        if self.validated_data["types"] == "Individual":
            member_serializer = IndividualMemberCreationSerializer(data=self.validated_data)
            if member_serializer.is_valid():
                member = member_serializer.create(self.validated_data)
                return member
        elif self.validated_data["types"] == "Company":
            member_serializer = CompanyMemberCreationSerializer(data=self.validated_data)
            if member_serializer.is_valid():
                member = member_serializer.create(self.validated_data)
                return member
        elif self.validated_data["types"] == "Partner":
            partner_serializer = PartnerCreationSerializer(data=self.validated_data)
            if partner_serializer.is_valid():
                partner = partner_serializer.create(self.validated_data)
                return partner


class RegistrationPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True, validators=[validate_password], max_length=128, min_length=6
    )
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True, validators=[validate_password], max_length=128, min_length=6
    )

    def save(self):
        account = User(
            email=self.validated_data['email'],
        )

        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match'})

        account.set_password(password)
        account.save()
        return account


# LOGIN
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    tokens = serializers.CharField(max_length=300, min_length=6, read_only=True)

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed('Invalid Credentials, try again')

        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')

        return {
            'email': user.email,
            'tokens': user.tokens
        }


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
