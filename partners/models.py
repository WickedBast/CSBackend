from django.db import models
from django.utils.translation import gettext_lazy as _
from communities.models import Community

from users.models import User


class Partner(models.Model):
    class Types(models.TextChoices):
        LOCAL = "LOCAL", "Local"
        CLEANSTOCK = "CLEANSTOCK", "CleanStock"

    class PartnerTypes(models.TextChoices):
        BANK = "BANK", "Bank"
        SERVICE_PROVIDER = "SERVICE PROVIDER", "Service Provider"
        ENERGY_COMPANY = "ENERGY COMPANY", "Energy Company"

    communities = models.ManyToManyField(Community, blank=True)

    type = models.CharField(_('Types'), max_length=30, choices=Types.choices, blank=True, null=True, default=Types.CLEANSTOCK)
    partner_type = models.CharField(_('Partner_Types'), max_length=30, choices=PartnerTypes.choices, blank=True,
                                    null=True)
    name = models.CharField(max_length=70, verbose_name="name", blank=True, null=True)
    phone_number = models.CharField(max_length=20, verbose_name="phone number", blank=True, null=True)
    nip_number = models.CharField(max_length=20, verbose_name="nip number", blank=True, null=True)
    zip_code = models.CharField(max_length=20, verbose_name="zip code", blank=True, null=True)
    address = models.CharField(max_length=100, verbose_name="address", blank=True, null=True)
    city = models.CharField(max_length=30, verbose_name="city", blank=True, null=True)

    energy_tariff = models.CharField(max_length=30, verbose_name="energy tariff", blank=True, null=True)
    pv_technology = models.CharField(max_length=30, verbose_name="pv technology", blank=True, null=True)
    pv_power_peak_installed = models.IntegerField(verbose_name="pv power peak installed", blank=True, null=True)
    system_loss = models.IntegerField(verbose_name="system loss", blank=True, null=True)
    mounting_position = models.CharField(max_length=20, verbose_name="mounting position", blank=True, null=True)
    slope = models.IntegerField(verbose_name="slope", blank=True, null=True)
    azimuth = models.IntegerField(verbose_name="azimuth", blank=True, null=True)

    class Meta:
        ordering = ["-id"]
        verbose_name = _("Partner")
        verbose_name_plural = _("Partners")

    def __str__(self):
        return self.name


class PartnerUsers(models.Model):
    partner = models.ForeignKey(Partner, models.CASCADE, null=True)
    users = models.OneToOneField(User, models.CASCADE, null=True)

    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)

    class Meta:
        ordering = ["-id"]
        verbose_name = _("User")
        verbose_name_plural = _("Users")
