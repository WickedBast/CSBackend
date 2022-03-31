from rest_framework import serializers
from partners.models import Partner


class PartnerCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = ['type', 'partner_type', 'name', 'phone_number', 'nip_number', 'zip_code', 'address', 'city',
                  'energy_tariff', 'pv_technology', 'pv_power_peak_installed', 'system_loss', 'mounting_position',
                  'slope', 'azimuth'
                  ]

    def create(self, validated_data):
        partner = Partner(
            type=self.validated_data['type'],
            partner_type=self.validated_data['partner_type'],
            name=self.validated_data['name'],
            phone_number=self.validated_data['phone_number'],
            nip_number=self.validated_data['nip_number'],
            zip_code=self.validated_data['zip_code'],
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
        partner.save()
        return partner
