from rest_framework import serializers
from communities.models import Community


class CommunityCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = ['type', 'community_name', 'zip_code', 'phone_number']

    def create(self, validated_data):
        community = Community(
            type=self.validated_data['type'],
            community_name=self.validated_data['community_name'],
            zip_code=self.validated_data['zip_code'],
            phone_number=self.validated_data['phone_number']
        )
        community.save()
        return community
