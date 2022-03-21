from rest_framework import serializers
from partners.models import Partner


class PartnerCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = ['type', 'partner_type', 'partner_name', 'phone_number', 'nip_number', 'zip_code']

    def create(self, validated_data):
        partner = Partner(
            type=self.validated_data['type'],
            partner_type=self.validated_data['partner_type'],
            partner_name=self.validated_data['partner_name'],
            phone_number=self.validated_data['phone_number'],
            nip_number=self.validated_data['nip_number'],
            zip_code=self.validated_data['zip_code']
        )
        partner.save()
        return partner
