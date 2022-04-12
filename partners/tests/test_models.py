from django.contrib.sites import requests
from django.test import TestCase
from partners.models import Partner, PartnerUsers

class BaseTestPartner(TestCase):
    def setUp(self) -> None:
        # location = requests.get(url="https://nominatim.openstreetmap.org/?",
        #                         params={
        #                             "city": community.city,
        #                             "street": community.address,
        #                             "postalcode": community.zip_code,
        #                             "format": "json",
        #                             "limit": 1,
        #                         })

        self.type = Partner.Types.CLEANSTOCK
        self.partner_type = Partner.PartnerTypes.SERVICE_PROVIDER
        self.name = "VivaDrive"
        self.phone_number = "123456789"
        self.nip_number = "789456123"
        self.zip_code = "00-236"
        self.address = "Dobra 56/66"
        self.city = "Warsaw"

        self.energy_tariff = "G12"



        # communities = models.ManyToManyField(Community, blank=True)
        #
        # energy_tariff = models.CharField(max_length=30, verbose_name="energy tariff", blank=True, null=True)
        # pv_technology = models.CharField(max_length=30, verbose_name="pv technology", blank=True, null=True)
        # pv_power_peak_installed = models.IntegerField(verbose_name="pv power peak installed", blank=True, null=True)
        # system_loss = models.IntegerField(verbose_name="system loss", blank=True, null=True)
        # mounting_position = models.CharField(max_length=20, verbose_name="mounting position", blank=True, null=True)
        # slope = models.IntegerField(verbose_name="slope", blank=True, null=True)
        # azimuth = models.IntegerField(verbose_name="azimuth", blank=True, null=True)

# class PartnerModel(TestCase):
#     def create(self):
