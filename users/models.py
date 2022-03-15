import os
from dotenv import load_dotenv
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from community.models import Community
from members.models import Member
from partner.models import Partner

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail

load_dotenv()


class AdministratorUser(BaseUserManager):
    def create_user(self, email, types, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            types=types
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, types, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            types=types
        )

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    class Types(models.TextChoices):
        INDIVIDUAL = "Individual", "INDIVIDUAL"
        ORGANIZATION = "Company", "COMPANY"
        PARTNER = "Partner", "PARTNER"

    community = models.ForeignKey(Community, on_delete=models.CASCADE, blank=True, null=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, blank=True, null=True)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, blank=True, null=True)

    email = models.EmailField(max_length=50, unique=True, verbose_name='email')
    password = models.CharField(max_length=128, verbose_name='password', blank=True, null=True)
    types = models.CharField(_('Types'), max_length=20, choices=Types.choices)

    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['types']

    objects = AdministratorUser()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'),
                                                   reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="CleanStock Account"),
        # message:
        email_plaintext_message,
        # from:
        os.getenv("DEFAULT_FROM_EMAIL"),
        # to:
        [reset_password_token.user.email]
    )
