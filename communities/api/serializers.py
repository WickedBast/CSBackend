from rest_framework import serializers
from communities.models import Community


class CommunityCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = ['type', 'name', 'zip_code', 'phone_number', 'address', 'city',
                  'energy_tariff', 'pv_technology', 'pv_power_peak_installed',
                  'system_loss', 'mounting_position', 'slope', 'azimuth'
                  ]

    def create(self, validated_data):
        community = Community(
            type=self.validated_data['type'],
            name=self.validated_data['name'],
            zip_code=self.validated_data['zip_code'],
            phone_number=self.validated_data['phone_number'],
            address=self.validated_data['address'],
            city=self.validated_data['city'],
            energy_tariff=self.validated_data['energy_tariff'],
            pv_technology=self.validated_data['pv_technology'],
            pv_power_peak_installed=self.validated_data['pv_power_peak_installed'],
            system_loss=self.validated_data['system_loss'],
            mounting_position=self.validated_data['mounting_position'],
            slope=self.validated_data['slope'],
            azimuth=self.validated_data['azimuth'],
        )
        community.save()
        return community
