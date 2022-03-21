from django.db import models
from django.utils.translation import gettext_lazy as _


class Community(models.Model):
    class Types(models.TextChoices):
        MUNICIPALITY = "MUNICIPALITY", "Municipality"
        COOPERATIVE = "COOPERATIVE", "Cooperative"

    # users = models.ManyToManyField(User, blank=True)

    type = models.CharField(_('Types'), max_length=20, choices=Types.choices)
    name = models.CharField(max_length=30, verbose_name="name")
    zip_code = models.CharField(max_length=20, verbose_name="zip code")
    phone_number = models.CharField(max_length=20, verbose_name="phone number")
    address = models.CharField(max_length=100, verbose_name="address")
    city = models.CharField(max_length=30, verbose_name="city")

    class Meta:
        ordering = ["-id"]
        verbose_name = _("Community")
        verbose_name_plural = _("Communities")

    def __str__(self):
        return self.name
