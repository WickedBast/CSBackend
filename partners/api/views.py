from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response

from partners.api import serializers
from partners.api.serializers import PartnerCreationSerializer
from partners.models import Partner


class PartnerCreationView(CreateAPIView):
    serializer_class = PartnerCreationSerializer
    permission_classes = []
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            partner = serializer.save()
            return Response({
                "response": "Partner Successfully Created.",
                "name": partner.name,
                "type": partner.type,
                "pk": partner.pk,
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "response": "Something went wrong!"
            }, status=status.HTTP_400_BAD_REQUEST)


class UpdateDataView(RetrieveUpdateAPIView):
    serializer_class = serializers.PartnerCreationSerializer
    permission_classes = []
    authentication_classes = []

    def get_queryset(self):
        return Partner.objects.all()
