from django.db import models
from django.utils.translation import gettext_lazy as _


class Community(models.Model):
    class Types(models.TextChoices):
        MUNICIPALITY = "MUNICIPALITY", "Municipality"
        COOPERATIVE = "COOPERATIVE", "Cooperative"

    type = models.CharField(_('Types'), max_length=20, choices=Types.choices)
    community_name = models.CharField(max_length=30, verbose_name="community name")
    zip_code = models.CharField(max_length=20, verbose_name="zip code")
    phone_number = models.CharField(max_length=20, verbose_name="phone number")

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.community_name
