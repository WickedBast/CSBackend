import re

import requests
from django.test import TestCase

from communities.models import Community
from partners.models import Partner, PartnerUsers
from users.models import User


class BaseTestPartner(TestCase):
    def setUp(self) -> None:
        loc = requests.get(url="https://nominatim.openstreetmap.org/?",
                           params={
                               "street": "Dobra 56/66",
                               "format": "json",
                               "addressdetails": 1,
                               "extratags": 1,
                               "limit": 1,
                           }).json()

        self.type = Partner.Types.CLEANSTOCK
        self.partner_type = Partner.PartnerTypes.SERVICE_PROVIDER
        self.name = "VivaDrive"
        self.phone_number = loc[0]["extratags"]["phone"]
        self.nip_number = "7894561230"
        self.zip_code = loc[0]["address"]["postcode"]
        self.address = loc[0]["address"]["road"] + " " + loc[0]["address"]["house_number"]
        self.city = loc[0]["address"]["city"]

        self.energy_tariff = "G12"
        self.pv_technology = "a24"
        self.pv_power_peak_installed = 19
        self.system_loss = 3
        self.mounting_position = "45"
        self.slope = 47
        self.azimuth = 31

        self.partner = Partner.objects.create(type=self.type,
                                              partner_type=self.partner_type,
                                              name=self.name,
                                              phone_number=self.phone_number,
                                              nip_number=self.nip_number,
                                              zip_code=self.zip_code,
                                              address=self.address,
                                              city=self.city,
                                              energy_tariff=self.energy_tariff,
                                              pv_technology=self.pv_technology,
                                              pv_power_peak_installed=self.pv_power_peak_installed,
                                              system_loss=self.system_loss,
                                              mounting_position=self.mounting_position,
                                              slope=self.slope,
                                              azimuth=self.azimuth)

        self.partner.save()

    def tearDown(self) -> None:
        self.partner.delete()


class PartnerModel(BaseTestPartner):
    def test_create_partner(self):
        self.assertTrue(isinstance(self.partner, Partner))

        self.assertEqual(self.partner.type, "cleanstock".upper())
        self.assertEqual(self.partner.partner_type, "service provider".upper())
        self.assertTrue(re.search('[a-zA-Z]', self.partner.name))
        self.assertTrue(re.search('[0-9]', self.phone_number))
        self.assertEqual(len(self.partner.nip_number), 10)
        self.assertTrue(self.partner.nip_number.isdigit())
        self.assertEqual(len(self.partner.zip_code), 6)
        self.assertTrue(self.partner.zip_code[:2].isdigit())
        self.assertTrue(self.partner.zip_code[3:].isdigit())
        self.assertTrue(self.partner.city.isalpha())

        self.assertEqual(self.partner.zip_code, "00-312")
        self.assertEqual(self.partner.address, "Dobra 56/66")
        self.assertEqual(self.partner.city, "Warszawa")

        self.assertTrue(isinstance(self.partner.pv_power_peak_installed, int))
        self.assertTrue(isinstance(self.partner.system_loss, int))
        self.assertTrue(isinstance(self.partner.slope, int))
        self.assertTrue(isinstance(self.partner.azimuth, int))

    def test_partner_community_relation(self):
        loc = requests.get(url="https://nominatim.openstreetmap.org/?",
                           params={
                               "street": "Wybrzeże Kościuszkowskie 20",
                               "format": "json",
                               "addressdetails": 1,
                               "extratags": 1,
                               "limit": 1,
                           }).json()

        community = Community.objects.create(type=Community.Types.COOPERATIVE,
                                             name=loc[0]["address"]["tourism"],
                                             zip_code=loc[0]["address"]["postcode"],
                                             phone_number=loc[0]["extratags"]["phone"],
                                             address=loc[0]["address"]["road"] + " " + loc[0]["address"][
                                                 "house_number"],
                                             city=loc[0]["address"]["city"],
                                             energy_tariff="G12",
                                             pv_technology="a24",
                                             pv_power_peak_installed=19,
                                             system_loss=3,
                                             mounting_position="45",
                                             slope=47,
                                             azimuth=31)

        community.save()

        self.partner.communities.set([community.pk])
        self.assertEqual(self.partner.communities.count(), 1)

        user = User.objects.create_user(email="user@gmail.com",
                                        types="Individual",
                                        password="")

        partner_user = PartnerUsers.objects.create(partner=self.partner, users=user)

        self.assertEqual(partner_user.partner.name, self.partner.__str__())
        self.assertEqual(partner_user.users.email, user.__str__())

    def test_partner_functions(self):
        self.assertEqual(self.partner.__str__(), self.partner.name)
        self.assertEqual(self.partner.__str__(), "VivaDrive")
