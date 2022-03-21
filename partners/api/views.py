from rest_framework.views import APIView
from rest_framework.response import Response

from django.utils.translation import gettext as _

from nip24 import *


class FleetNip(APIView):

    def get(self, request, nip):

        id = "5gOElQTlpEZl"
        key = "FCv4dvZz0tHe"
        nip24 = NIP24Client(id, key)

        all = nip24.getAllDataExt(Number.NIP, nip)
        if all:
            response = {
                "company_name": all.name,
                "nip": all.nip,
                "street": all.street,
                "streetNumber": all.streetNumber,
                "houseNumber": all.houseNumber,
                "city": all.city,
                "postCode": all.postCode,
                "postCity": all.postCity,
            }
            try:
                address = response["street"] + " " + response["streetNumber"] + " " + response["houseNumber"]

                pkpcode = [
                    {
                        "code": al.code,
                        "primary": al.primary,
                    } for al in all.pkd[0:3]
                ]
            except Exception as e:
                print(e)
            return Response(response)

        else:
            return Response({"error": _("NIP not found")})


'''
                models.CompanyLead.objects.create(
                    company_name=response["company_name"],
                    company_nip=response["nip"],
                    company_regon=all.regon, 
                    address=address,
                    postcode=response["postCode"],
                    city=response["city"],
                    pkp_codes=pkpcode,
                    phone=all.phone,
                    email=all.email)
'''
