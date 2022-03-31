from rest_framework import serializers
from members.models import Member


class MemberCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['first_name', 'last_name', 'organization_name', 'nip_number',
                  'type', 'phone_number', 'energy_tariff',
                  'pv_technology', 'pv_power_peak_installed',
                  'system_loss', 'mounting_position', 'slope', 'azimuth',
                  'address', 'city', 'zip_code']

    def create(self, validated_data):
        if 'first_name' in self.validated_data.keys():
            member = Member(
                first_name=self.validated_data['first_name'],
                last_name=self.validated_data['last_name'],
                type=self.validated_data['type'],
                phone_number=self.validated_data['phone_number'],
                energy_tariff=self.validated_data['energy_tariff'],
                pv_technology=self.validated_data['pv_technology'],
                pv_power_peak_installed=self.validated_data['pv_power_peak_installed'],
                system_loss=self.validated_data['system_loss'],
                mounting_position=self.validated_data['mounting_position'],
                slope=self.validated_data['slope'],
                azimuth=self.validated_data['azimuth'],
                address=self.validated_data['address'],
                city=self.validated_data['city'],
                zip_code=self.validated_data['zip_code']
            )
            member.save()
            return member
        elif 'organization_name' in self.validated_data.keys():
            member = Member(
                organization_name=self.validated_data['organization_name'],
                nip_number=self.validated_data['nip_number'],
                type=self.validated_data['type'],
                phone_number=self.validated_data['phone_number'],
                energy_tariff=self.validated_data['energy_tariff'],
                pv_technology=self.validated_data['pv_technology'],
                pv_power_peak_installed=self.validated_data['pv_power_peak_installed'],
                system_loss=self.validated_data['system_loss'],
                mounting_position=self.validated_data['mounting_position'],
                slope=self.validated_data['slope'],
                azimuth=self.validated_data['azimuth'],
                address=self.validated_data['address'],
                city=self.validated_data['city'],
                zip_code=self.validated_data['zip_code']
            )
            member.save()
            return member


class DashboardSerializer(serializers.Serializer):
    displayName = serializers.SerializerMethodField(read_only=True)

    def get_displayName(self, obj):
        return self.context["request"].member.get_full_name()
