from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from nip24 import *


class CompanyNIP(APIView):
    def get(self, request, nip):
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
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response({"error": _("NIP not found")}, status=status.HTTP_404_NOT_FOUND)
