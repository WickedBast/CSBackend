from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from users.models import User
from members.models import Member
from community.models import Community
from partner.models import Partner
from django.contrib import auth


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'type']

    def save(self):
        account = User(
            email=self.validated_data['email'],
            type=self.validated_data['type']
        )

        account.save()
        return account


class MemberCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['type', 'phone_number', 'energy_tariff', 'pv_technology',
                  'pv_power_peak_installed', 'system_loss', 'mounting_position',
                  'slope', 'azimuth']

    def save(self):
        member = Member(
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            organization_name=self.validated_data['organization_name'],
            nip_number=self.validated_data['nip_number'],
            type="PROSPECT",
            phone_number=self.validated_data['phone_number'],
            energy_tariff=self.validated_data['energy_tariff'],
            pv_technology=self.validated_data['pv_technology'],
            pv_power_peak_installed=self.validated_data['pv_power_peak_installed'],
            system_loss=self.validated_data['system_loss'],
            mounting_position=self.validated_data['mounting_position'],
            slope=self.validated_data['slope'],
            azimuth=self.validated_data['azimuth']
        )
        member.save()
        return member


class CommunityCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = ['type', 'community_name', 'zip_code', 'phone_number']

    def save(self):
        community = Community(
            type=self.validated_data['type'],
            community_name=self.validated_data['community_name'],
            zip_code=self.validated_data['zip_code'],
            phone_number=self.validated_data['phone_number']
        )
        community.save()
        return community


class PartnerCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = ['']


class RegistrationPasswordSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

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


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    tokens = serializers.CharField(max_length=300, min_length=6, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'tokens']

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


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('old_password', 'new_password', 'confirm_new_password')
