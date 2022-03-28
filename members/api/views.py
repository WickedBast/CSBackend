from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.views import APIView
from members.api import serializers
from members.models import Member
from CSBackend.utils import OIsAuthenticated


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


# class DashboardView(RetrieveAPIView):
#     permission_classes = [OIsAuthenticated]
#     serializer_class = serializers.DashboardSerializer

class DashboardView(RetrieveAPIView):
    permission_classes = []
    serializer_class = serializers.DashboardSerializer

    def get(self, request, *args, **kwargs):
        return Response({
            "first_name": "Dinesh",
            "second_name": "Kumar",
        })

