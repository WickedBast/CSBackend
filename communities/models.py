from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User


class Community(models.Model):
    class Types(models.TextChoices):
        MUNICIPALITY = "MUNICIPALITY", "Municipality"
        COOPERATIVE = "COOPERATIVE", "Cooperative"

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


class CommunityUsers(models.Model):
    community = models.ForeignKey(Community, models.CASCADE, null=True)
    users = models.OneToOneField(User, models.CASCADE, null=True)

    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)

    class Meta:
        ordering = ["-id"]
        verbose_name = _("User")
        verbose_name_plural = _("Users")
