from django.db import models
from community.models import Community


class Member(models.Model):
    class Types(models.TextChoices):
        PROSPECT = "PROSPECT", "Prospect"
        SCHOOL = "SCHOOL", "School"
        PROSUMENT = "PROSUMENT", "Prosument"
        BENEFICIARY = "BENEFICIARY", "Beneficiary"

    community = models.ForeignKey(Community, on_delete=models.CASCADE)

    type = models.CharField(max_length=20, choices=Types.choices)
    first_name = models.CharField(max_length=30, verbose_name="first name", blank=True, null=True)
    last_name = models.CharField(max_length=30, verbose_name="last name", blank=True, null=True)
    organization_name = models.CharField(max_length=50, verbose_name="organization name", blank=True, null=True)
    nip_number = models.CharField(max_length=10, verbose_name="nip number", blank=True, null=True)
    phone_number = models.CharField(max_length=20, verbose_name="phone number")
    energy_tariff = models.CharField(max_length=30, verbose_name="energy tariff", blank=True, null=True)

    pv_technology = models.CharField(max_length=30, verbose_name="pv technology", blank=True, null=True)
    pv_power_peak_installed = models.IntegerField(verbose_name="pv power peak installed", blank=True, null=True)
    system_loss = models.IntegerField(verbose_name="system loss", blank=True, null=True)
    mounting_position = models.CharField(max_length=20, verbose_name="mounting position", blank=True, null=True)
    slope = models.IntegerField(verbose_name="slope", blank=True, null=True)
    azimuth = models.IntegerField(verbose_name="azimuth", blank=True, null=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.first_name
