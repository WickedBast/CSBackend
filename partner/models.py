from django.db import models
from django.utils.translation import gettext_lazy as _
from community.models import Community


class Partner(models.Model):
    class Types(models.TextChoices):
        LOCAL = "LOCAL", "Local"
        CLEANSTOCK = "CLEANSTOCK", "CleanStock"

    class PartnerTypes(models.TextChoices):
        BANK = "BANK", "Bank"
        SERVICE_PROVIDER = "SERVICE PROVIDER", "Service Provider"
        ENERGY_COMPANY = "ENERGY COMPANY", "Energy Company"

    community = models.ManyToManyField(Community, blank=True)

    type = models.CharField(_('Types'), max_length=30, choices=Types.choices)
    partner_type = models.CharField(_('Partner_Types'), max_length=30, choices=PartnerTypes.choices, blank=True, null=True)
    partner_name = models.CharField(max_length=30, verbose_name="partner name")
    phone_number = models.CharField(max_length=20, verbose_name="phone number")
    nip_number = models.CharField(max_length=20, verbose_name="nip number", blank=True, null=True)
    zip_code = models.CharField(max_length=20, verbose_name="zip code")

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.partner_name
