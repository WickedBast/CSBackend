import os

import requests
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.utils.translation import gettext as _
from django_rest_passwordreset import models
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from communities.models import Community, CommunityUsers
from members.models import Member, MemberUsers
from partners.models import Partner, PartnerUsers
from users.models import User


# REGISTRATION
class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True, max_length=50)
    types = serializers.CharField(write_only=True)
    type = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(write_only=True)
    address = serializers.CharField(write_only=True)
    city = serializers.CharField(write_only=True)
    zip_code = serializers.CharField(write_only=True)
    name = serializers.CharField(write_only=True, required=False)
    companyName = serializers.CharField(write_only=True, required=False)
    nip_number = serializers.CharField(write_only=True, required=False)
    partner_type = serializers.CharField(write_only=True, required=False)
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)

    # havePV = serializers.BooleanField(write_only=True, required=False)
    # taxNumber = serializers.CharField(write_only=True, required=False)
    # technology = serializers.CharField(write_only=True, required=False)
    # installedPeakPVPower = serializers.CharField(write_only=True, required=False)
    # systemLoss = serializers.CharField(write_only=True, required=False)
    # mountingPosition = serializers.CharField(write_only=True, required=False)
    # slope = serializers.CharField(write_only=True, required=False)
    # azimuth = serializers.CharField(write_only=True, required=False)

    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            types=validated_data["types"],
        )
        # try:
        if self.validateEmail(validated_data["email"]):
            # Save the user
            user.save()

            # Create the registration token
            token = models.ResetPasswordToken.objects.create(user=user)
            token.save()

            # Send the confirmation email
            self.send_confirmation_email(user=user, token=token.key)

            # Create the data model and link with the user
            self.save_type(validated_data=validated_data, user=user)

        # except:
        #     try:
        #         user.delete()
        #         models.ResetPasswordToken.objects.get(user=user).delete()
        #         raise ValidationError({"email": [_("User already exists")]})
        #     except:
        #         raise ValidationError({"email": [_("User already exists")]})

        return user

    def send_confirmation_email(self, user, token):
        return requests.post(
            "https://api.eu.mailgun.net/v3/cleanstock.eu/messages",
            auth=("api", os.getenv("MAILGUN_API_KEY")),
            data={"from": "Clean Stock Team <noreply@cleanstock.eu>",
                  "to": user.email,
                  "subject": "Welcome to Clean Stock",
                  "template": "confirm_email",
                  "v:domain": "54.38.139.134",
                  "v:token": f"{token}",
                  }
        )

    def validateEmail(self, email):
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False

    def save_type(self, validated_data, user):
        if user.types == "Individual":
            # Create the necessary data model
            member = Member.objects.create(
                type=validated_data["type"],
                phone_number=validated_data["phone_number"],
                zip_code=validated_data["zip_code"],
                address=validated_data["address"],
                city=validated_data["city"],
                first_name=validated_data["first_name"],
                last_name=validated_data["last_name"],
                energy_tariff=validated_data["taxNumber"]
            )
            # if validated_data["havePV"]:
            #     member.pv_technology = validated_data["technology"]
            #     member.pv_power_peak_installed = validated_data["installedPeakPVPower"]
            #     member.system_loss = validated_data["systemLoss"]
            #     member.mounting_position = validated_data["mountingPosition"]
            #     member.slope = validated_data["slope"]
            #     member.azimuth = validated_data["azimuth"]

            member.save()

            # Create the necessary data model's user to link with the actual user
            member_user = MemberUsers.objects.create(users=user, member=member)
            member_user.save()

        elif user.types == "Company":
            # Create the necessary data model
            member = Member.objects.create(
                type=validated_data["type"],
                phone_number=validated_data["phone_number"],
                zip_code=validated_data["zip_code"],
                address=validated_data["address"],
                city=validated_data["city"],
                organization_name=validated_data["companyName"],
                nip_number=validated_data["nip_number"],
                energy_tariff=validated_data["taxNumber"]
            )
            # if validated_data["havePV"]:
            #     member.pv_technology = validated_data["technology"]
            #     member.pv_power_peak_installed = validated_data["installedPeakPVPower"]
            #     member.system_loss = validated_data["systemLoss"]
            #     member.mounting_position = validated_data["mountingPosition"]
            #     member.slope = validated_data["slope"]
            #     member.azimuth = validated_data["azimuth"]

            member.save()

            # Create the necessary data model's user to link with the actual user
            member_user = MemberUsers.objects.create(users=user, member=member)
            member_user.save()

        elif user.types == "Partner":
            # Create the necessary data model
            partner = Partner.objects.create(
                type=validated_data["type"],
                partner_type=validated_data["partner_type"],
                name=validated_data["name"],
                phone_number=validated_data["phone_number"],
                nip_number=validated_data["nip_number"],
                zip_code=validated_data["zip_code"],
                address=validated_data["address"],
                city=validated_data["city"],
                energy_tariff=validated_data["taxNumber"]
            )
            # if validated_data["havePV"]:
            #     partner.pv_technology = validated_data["technology"]
            #     partner.pv_power_peak_installed = validated_data["installedPeakPVPower"]
            #     partner.system_loss = validated_data["systemLoss"]
            #     partner.mounting_position = validated_data["mountingPosition"]
            #     partner.slope = validated_data["slope"]
            #     partner.azimuth = validated_data["azimuth"]

            partner.save()

            # Create the necessary data model's user to link with the actual user
            partner_user = PartnerUsers.objects.create(users=user, partner=partner)
            partner_user.save()

        elif user.types == "Community":
            # Create the necessary data model
            community = Community.objects.create(
                type=validated_data["type"],
                name=validated_data["name"],
                zip_code=validated_data["zip_code"],
                phone_number=validated_data["phone_number"],
                address=validated_data["address"],
                city=validated_data["city"],
                energy_tariff=validated_data["taxNumber"]
            )
            # if validated_data["havePV"]:
            #     community.pv_technology = validated_data["technology"]
            #     community.pv_power_peak_installed = validated_data["installedPeakPVPower"]
            #     community.system_loss = validated_data["systemLoss"]
            #     community.mounting_position = validated_data["mountingPosition"]
            #     community.slope = validated_data["slope"]
            #     community.azimuth = validated_data["azimuth"]

            community.save()

            # Create the necessary data model's user to link with the actual user
            community_member = CommunityUsers.objects.create(users=user, community=community)
            community_member.save()


class RegistrationPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True, validators=[validate_password], max_length=128, min_length=6
    )
    token = serializers.CharField()


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
