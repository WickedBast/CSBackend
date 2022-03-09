from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from community.models import Community
from members.models import Member
from partner.models import Partner


class AdministratorUser(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        user = self.create_user(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            password=password
        )

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    class Types(models.TextChoices):
        INDIVIDUAL = "INDIVIDUAL", "Individual"
        ORGANIZATION = "ORGANIZATION", "Organization"
        PARTNER = "PARTNER", "Partner"

    community = models.ForeignKey(Community, on_delete=models.CASCADE, blank=True, null=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, blank=True, null=True)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, blank=True, null=True)

    email = models.EmailField(max_length=50, unique=True, verbose_name='email', primary_key=True)
    first_name = models.CharField(max_length=30, verbose_name='first name')
    last_name = models.CharField(max_length=30, verbose_name='last name')
    type = models.CharField(_('Types'), max_length=20, choices=Types.choices)

    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = AdministratorUser()

    def __str__(self):
        return self.email

    def name(self):
        return self.first_name + " " + self.last_name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
