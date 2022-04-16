from django.test import TestCase
from partners.models import Partner
import requests


class PartnerRegistration(TestCase):
    def test_partner_register_api(self):
        loc = requests.get(url="https://nominatim.openstreetmap.org/?",
                           params={
                               "street": "Dobra 56/66",
                               "format": "json",
                               "addressdetails": 1,
                               "extratags": 1,
                               "limit": 1,
                           }).json()

        data = {
            "type": Partner.Types.CLEANSTOCK,
            "partner_type": Partner.PartnerTypes.SERVICE_PROVIDER,
            "name": "VivaDrive",
            "phone_number": loc[0]["extratags"]["phone"],
            "nip_number": "789456123",
            "zip_code": loc[0]["address"]["postcode"],
            "address": loc[0]["address"]["road"] + " " + loc[0]["address"]["house_number"],
            "city": loc[0]["address"]["city"],
            "energy_tariff": "G12",
            "pv_technology": "a24",
            "pv_power_peak_installed": 19,
            "system_loss": 3,
            "mounting_position": "45",
            "slope": 47,
            "azimuth": 31
        }

        response = self.client.post("/register/", data=data)
        self.assertEqual(Partner.objects.count(), 0)  # 1
        self.assertEqual(response.status_code, 404)  # 201
