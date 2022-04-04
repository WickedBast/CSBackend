from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


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
