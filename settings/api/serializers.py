from rest_framework import serializers


class ContactDetailsSerializer(serializers.Serializer):
    user = serializers.CurrentUserDefault
