from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from django.utils.translation import gettext as _
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email

from members.api.serializers import (
    IndividualMemberCreationSerializer,
    CompanyMemberCreationSerializer,
)
from partners.api.serializers import (
    PartnerCreationSerializer
)

from users.models import User
from members.models import Member, MemberUsers
from partners.models import Partner, PartnerUsers
from django.contrib import auth


# REGISTRATION
class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True, max_length=50)
    types = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            types=validated_data["types"],
        )
        try:
            if self.validateEmail(validated_data["email"]):
                if user.types == "Individual" or "Company":
                    member = self.save_type()
                    member_user = MemberUsers.objects.get(member=member)
                    member_user.member = member
                    member_user.users.save(user)
                elif user.types == "Partner":
                    partner = self.save_type()
                    partner_user = PartnerUsers.objects.get(partner=partner)
                    partner_user.partner = partner
                    partner_user.users.save(user)
                user.save()
        except:
            raise ValidationError({"email": [_("User already exists")]})

        return user

    def validateEmail(self, email):
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False

    def save_type(self):
        if self.validated_data["types"] == "Individual":
            member_serializer = IndividualMemberCreationSerializer()
            if member_serializer.is_valid():
                member = member_serializer.create(self.validated_data)
                return member
        elif self.validated_data["types"] == "Company":
            member_serializer = CompanyMemberCreationSerializer()
            if member_serializer.is_valid():
                member = member_serializer.create(self.validated_data)
                return member
        elif self.validated_data["types"] == "Partner":
            partner_serializer = PartnerCreationSerializer()
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
