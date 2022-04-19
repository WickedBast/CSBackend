import requests
from django.utils.translation import gettext as _
from nip24 import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_api_key.models import APIKey

from CSBackend.serializers import ZIPSerializer, NIPSerializer
from communities.models import Community


class CompanyNIP(APIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = NIPSerializer

    def post(self, request):
        data = request.data
        try:
            api = APIKey.objects.get_from_key(key=data["api_key"]).name == "NIP"
            if not api:
                raise Error
        except APIKey.DoesNotExist:
            return Response({"error:": _("API Key Does not Exist")}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"error:": _("Wrong API Key")}, status=status.HTTP_403_FORBIDDEN)

        ID = os.getenv("NIP_ID")
        KEY = os.getenv("NIP_KEY")
        nip24 = NIP24Client(id=ID, key=KEY)
        data = nip24.getAllDataExt(Number.NIP, data["nip"])

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


class MapZIP(APIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = ZIPSerializer

    def post(self, request):
        data = request.data
        try:
            api = APIKey.objects.get_from_key(key=data["api_key"]).name == "ZIP"
            if not api:
                raise Error
        except APIKey.DoesNotExist:
            return Response({"error:": _("API Key Does not Exist")}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"error:": _("Wrong API Key")}, status=status.HTTP_403_FORBIDDEN)

        is_empty = requests.get(url="https://nominatim.openstreetmap.org/?",
                                params={
                                    "postalcode": data["zip"],
                                    "format": "json",
                                    "limit": 1,
                                })

        if is_empty.text == "[]":
            return Response({"error": _("Invalid ZIP")}, status=status.HTTP_400_BAD_REQUEST)

        communities = Community.objects.filter(zip_code__istartswith=data["zip"][:3]).all()
        locations = []
        for community in communities:
            location = requests.get(url="https://nominatim.openstreetmap.org/?",
                                    params={
                                        "q": community.name,
                                        "city": community.city,
                                        "street": community.address,
                                        "postalcode": community.zip_code,
                                        "format": "json",
                                        "limit": 1,
                                    })
            if location.text == "[]":
                location = requests.get(url="https://nominatim.openstreetmap.org/?",
                                        params={
                                            "city": community.city,
                                            "street": community.address,
                                            "postalcode": community.zip_code,
                                            "format": "json",
                                            "limit": 1,
                                        })
            loc = location.json()
            value = {
                "name": community.name,
                "zip": community.zip_code,
                "city": community.city,
                "lat": loc[0]["lat"],
                "lon": loc[0]["lon"]
            }
            locations.append(value)

        if len(locations) == 0:
            return Response({"warning": _("No communities in this ZIP")}, status=status.HTTP_202_ACCEPTED)

        return Response(locations, status=status.HTTP_202_ACCEPTED)
