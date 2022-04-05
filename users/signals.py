import os

import requests
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    requests.post(
        "https://api.eu.mailgun.net/v3/cleanstock.eu/messages",
        auth=("api", os.getenv("MAILGUN_API_KEY")),
        data={"from": "Clean Stock Team <noreply@cleanstock.eu>",
              "to": reset_password_token.user.email,
              "subject": "Password Reset for Clean Stock Account",
              "template": "confirm_email",
              "v:reset_password_url": "{}?token={}".format(
                  instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
                  reset_password_token.key),
              }
    )
