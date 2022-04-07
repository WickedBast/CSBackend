from django.db import models
from communities.models import Community
from users.models import User
from django.utils.translation import gettext_lazy as _


class Member(models.Model):
    class Types(models.TextChoices):
        PROSPECT = "PROSPECT", "Prospect"
        SCHOOL = "SCHOOL", "School"
        PROSUMENT = "PROSUMENT", "Prosument"
        BENEFICIARY = "BENEFICIARY", "Beneficiary"

    community = models.ForeignKey(Community, on_delete=models.CASCADE, blank=True, null=True)

    type = models.CharField(max_length=30, choices=Types.choices)
    first_name = models.CharField(max_length=50, verbose_name="first name", blank=True, null=True)
    last_name = models.CharField(max_length=50, verbose_name="last name", blank=True, null=True)
    organization_name = models.CharField(max_length=70, verbose_name="organization name", blank=True, null=True)
    nip_number = models.CharField(max_length=10, verbose_name="nip number", blank=True, null=True)
    phone_number = models.CharField(max_length=20, verbose_name="phone number")
    zip_code = models.CharField(max_length=10, verbose_name="zip code")
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
        verbose_name = _("Member")
        verbose_name_plural = _("Members")

    def __str__(self):
        return self.first_name or self.organization_name

    def get_full_name(self):
        return self.first_name + " " + self.last_name


class MemberUsers(models.Model):
    member = models.ForeignKey(Member, models.CASCADE, null=True)
    users = models.OneToOneField(User, models.CASCADE, null=True)

    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)

    class Meta:
        ordering = ["-id"]
        verbose_name = _("User")
        verbose_name_plural = _("Users")
