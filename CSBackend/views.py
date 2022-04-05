from django.utils.translation import gettext as _
from nip24 import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework_api_key.models import APIKey


class CompanyNIP(APIView):
    permission_classes = [HasAPIKey]
    authentication_classes = []

    def get(self, request, nip):
        key = request.META["HTTP_X_API_KEY"].split()[0]
        if APIKey.objects.get_from_key(key=key):
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
            return Response({"error:": _("Wrong API Key")}, status=status.HTTP_403_FORBIDDEN)
