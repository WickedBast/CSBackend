import re

import requests
from django.test import TestCase

from communities.models import Community
from members.models import Member, MemberUsers
from users.models import User


class BaseTestIndividualMember(TestCase):
    def setUp(self) -> None:
        loc = requests.get(url="https://nominatim.openstreetmap.org/?",
                           params={
                               "street": "Janusza Meissnera 6",
                               "city": "Warsaw",
                               "format": "json",
                               "addressdetails": 1,
                               "extratags": 1,
                               "limit": 1,
                           }).json()

        self.type = Member.Types.PROSPECT
        self.first_name = "Ogul"
        self.last_name = "Tutuncu"
        self.phone_number = "456789132"
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

        self.member = Member.objects.create(type=self.type,
                                            first_name=self.first_name,
                                            last_name=self.last_name,
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

        self.member.save()

    def tearDown(self) -> None:
        self.member.delete()


class BaseTestCompanyMember(TestCase):
    def setUp(self) -> None:
        loc = requests.get(url="https://nominatim.openstreetmap.org/?",
                           params={
                               "street": "Janusza Meissnera 6",
                               "city": "Warsaw",
                               "format": "json",
                               "addressdetails": 1,
                               "extratags": 1,
                               "limit": 1,
                           }).json()

        self.type = Member.Types.PROSPECT
        self.organization_name = "E&T"
        self.nip_number = "1237894560"
        self.phone_number = "456789132"
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

        self.member = Member.objects.create(type=self.type,
                                            organization_name=self.organization_name,
                                            nip_number=self.nip_number,
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

        self.member.save()

    def tearDown(self) -> None:
        super().tearDown()


class IndividualMemberModel(BaseTestIndividualMember):
    def test_create_individual_member(self):
        self.assertTrue(isinstance(self.member, Member))

        self.assertEqual(self.member.type, "prospect".upper())
        self.assertTrue(re.search('[a-zA-Z]', self.member.first_name))
        self.assertTrue(re.search('[a-zA-Z]', self.member.last_name))
        self.assertTrue(re.search('[0-9]', self.phone_number))
        self.assertEqual(len(self.member.zip_code), 6)
        self.assertTrue(self.member.zip_code[:2].isdigit())
        self.assertTrue(self.member.zip_code[3:].isdigit())
        self.assertTrue(self.member.city.isalpha())

        self.assertEqual(self.member.zip_code, "03-982")
        self.assertEqual(self.member.address, "Janusza Meissnera 6")
        self.assertEqual(self.member.city, "Warszawa")

        self.assertTrue(isinstance(self.member.pv_power_peak_installed, int))
        self.assertTrue(isinstance(self.member.system_loss, int))
        self.assertTrue(isinstance(self.member.slope, int))
        self.assertTrue(isinstance(self.member.azimuth, int))

    def test_individual_member_community_relation(self):
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

        self.member.community = community
        self.assertTrue(isinstance(self.member.community, Community))
        self.assertEqual(self.member.community.name, community.name)
        self.assertEqual(self.member.community.name, "Centrum Nauki Kopernik")

        user = User.objects.create_user(email="user@gmail.com",
                                        types="Individual",
                                        password="")

        member_user = MemberUsers.objects.create(member=self.member, users=user)

        self.assertEqual(member_user.member.first_name, self.member.__str__())
        self.assertEqual(member_user.users.email, user.__str__())

    def test_member_functions(self):
        self.assertEqual(self.member.__str__(), self.member.first_name)
        self.assertEqual(self.member.__str__(), "Ogul")
        self.assertEqual(self.member.get_full_name(), self.member.first_name + " " + self.member.last_name)
        self.assertEqual(self.member.get_full_name(), "Ogul Tutuncu")


class CompanyMemberModel(BaseTestCompanyMember):
    def test_create_company_member(self):
        self.assertTrue(isinstance(self.member, Member))

        self.assertEqual(self.member.type, "prospect".upper())
        self.assertTrue(re.search('[a-zA-Z]', self.member.organization_name))
        self.assertEqual(len(self.member.nip_number), 10)
        self.assertTrue(self.member.nip_number.isdigit())
        self.assertTrue(re.search('[0-9]', self.phone_number))
        self.assertEqual(len(self.member.zip_code), 6)
        self.assertTrue(self.member.zip_code[:2].isdigit())
        self.assertTrue(self.member.zip_code[3:].isdigit())
        self.assertTrue(self.member.city.isalpha())

        self.assertEqual(self.member.zip_code, "03-982")
        self.assertEqual(self.member.address, "Janusza Meissnera 6")
        self.assertEqual(self.member.city, "Warszawa")

        self.assertTrue(isinstance(self.member.pv_power_peak_installed, int))
        self.assertTrue(isinstance(self.member.system_loss, int))
        self.assertTrue(isinstance(self.member.slope, int))
        self.assertTrue(isinstance(self.member.azimuth, int))

    def test_company_member_community_relation(self):
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

        self.member.community = community
        self.assertTrue(isinstance(self.member.community, Community))
        self.assertEqual(self.member.community.name, community.name)
        self.assertEqual(self.member.community.name, "Centrum Nauki Kopernik")

        user = User.objects.create_user(email="user@gmail.com",
                                        types="Individual",
                                        password="")

        member_user = MemberUsers.objects.create(member=self.member, users=user)

        self.assertEqual(member_user.member.organization_name, self.member.__str__())
        self.assertEqual(member_user.users.email, user.__str__())

    def test_member_functions(self):
        self.assertEqual(self.member.__str__(), self.member.organization_name)
        self.assertEqual(self.member.__str__(), "E&T")

