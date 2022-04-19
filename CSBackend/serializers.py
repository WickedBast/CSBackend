from rest_framework import serializers


class ZIPSerializer(serializers.Serializer):
    api_key = serializers.CharField(write_only=True, required=True)
    zip = serializers.CharField(write_only=True, required=True)