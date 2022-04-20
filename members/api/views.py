from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response

from members.api import serializers
from members.models import Member


class MemberCreationView(CreateAPIView):
    serializer_class = serializers.MemberCreationSerializer
    permission_classes = []
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            member = serializer.save()
            return Response({
                "response": "Member Successfully Created.",
                "type": member.type,
                "pk": member.pk,
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "response": "Something went wrong!"
            }, status=status.HTTP_400_BAD_REQUEST)


class UpdateDataView(RetrieveUpdateAPIView):
    serializer_class = serializers.MemberCreationSerializer
    permission_classes = []
    authentication_classes = []

    def get_queryset(self):
        return Member.objects.all()
