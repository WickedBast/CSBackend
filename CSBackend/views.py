import os

from django.utils.translation import gettext as _
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from nip24 import *


class CompanyNIP(APIView):
    permission_classes = []
    authentication_classes = []

    key = openapi.Parameter('key', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, required=True)

    @swagger_auto_schema(manual_parameters=[key])
    def get(self, request, nip):
        api_key = os.getenv("API_KEY")
        if request.GET.get('key') == api_key:
            ID = os.getenv("NIP_ID")
            KEY = os.getenv("NIP_KEY")
            nip24 = NIP24Client(id=ID, key=KEY)
            data = nip24.getAllDataExt(Number.NIP, nip)

            if data:
                response = {
                    "company_name": data.name,
                    "nip": data.nip,
                    "street": data.street,
                    "streetNumber": data.streetNumber,
                    "houseNumber": data.houseNumber,
                    "city": data.city,
                    "postCode": data.postCode,
                    "postCity": data.postCity,
                    "regon": data.regon,
                }
                return Response(response, status=status.HTTP_200_OK)
            else:
                return Response({"error": _("NIP not found")}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": _("Wrong API KEY")}, status=status.HTTP_400_BAD_REQUEST)
