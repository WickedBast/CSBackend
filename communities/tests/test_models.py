import re

import requests
from django.test import TestCase
from communities.models import Community, CommunityUsers
from users.models import User


class BaseTestCommunity(TestCase):
    def setUp(self) -> None:
        loc = requests.get(url="https://nominatim.openstreetmap.org/?",
                           params={
                               "street": "plac Defilad 1",
                               "format": "json",
                               "addressdetails": 1,
                               "extratags": 1,
                               "limit": 1,
                           }).json()

        self.type = Community.Types.COOPERATIVE
        self.name = loc[0]["address"]["historic"]
        self.phone_number = "741963852"
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

        self.community = Community.objects.create(type=self.type,
                                                  name=self.name,
                                                  phone_number=self.phone_number,
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

        self.community.save()

        self.community.save()

    def tearDown(self) -> None:
        self.community.delete()


class CommunityModel(BaseTestCommunity):
    def test_create_community(self):
        self.assertTrue(isinstance(self.community, Community))

        self.assertEqual(self.community.type, "cooperative".upper())
        self.assertTrue(re.search('[a-zA-Z]', self.community.name))
        self.assertTrue(re.search('[0-9]', self.phone_number))
        self.assertEqual(len(self.community.zip_code), 6)
        self.assertTrue(self.community.zip_code[:2].isdigit())
        self.assertTrue(self.community.zip_code[3:].isdigit())
        self.assertTrue(self.community.city.isalpha())

        self.assertEqual(self.community.zip_code, "00-110")
        self.assertEqual(self.community.address, "Plac Defilad 1")
        self.assertEqual(self.community.city, "Warszawa")

        self.assertTrue(isinstance(self.community.pv_power_peak_installed, int))
        self.assertTrue(isinstance(self.community.system_loss, int))
        self.assertTrue(isinstance(self.community.slope, int))
        self.assertTrue(isinstance(self.community.azimuth, int))

    def test_community_relation(self):
        user = User.objects.create_user(email="user@gmail.com",
                                        types="Individual",
                                        password="")

        community_user = CommunityUsers.objects.create(community=self.community, users=user)

        self.assertEqual(community_user.community.name, self.community.__str__())
        self.assertEqual(community_user.users.email, user.__str__())

    def test_member_functions(self):
        self.assertEqual(self.community.__str__(), self.community.name)
        self.assertEqual(self.community.__str__(), "Pałac Kultury")
