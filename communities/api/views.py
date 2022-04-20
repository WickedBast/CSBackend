from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response

from communities.api import serializers
from communities.api.serializers import CommunityCreationSerializer
from communities.models import Community


class CommunityCreationView(CreateAPIView):
    serializer_class = CommunityCreationSerializer
    permission_classes = []
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            community = serializer.save()
            return Response({
                "response": "Community Successfully Created.",
                "type": community.type,
                "pk": community.pk,
                "name": community.name,
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "response": "Something went wrong!"
            }, status=status.HTTP_400_BAD_REQUEST)


class UpdateDataView(RetrieveUpdateAPIView):
    serializer_class = serializers.CommunityCreationSerializer
    permission_classes = []
    authentication_classes = []

    def get_queryset(self):
        return Community.objects.all()
