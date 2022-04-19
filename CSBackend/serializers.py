from rest_framework import serializers


class ZIPSerializer(serializers.Serializer):
    api_key = serializers.CharField(write_only=True, required=True)
    zip = serializers.CharField(write_only=True, required=True)


class NIPSerializer(serializers.Serializer):
    api_key = serializers.CharField(write_only=True, required=True)
    nip = serializers.CharField(write_only=True, required=True)
