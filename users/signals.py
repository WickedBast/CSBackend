import os
from dotenv import load_dotenv
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import EmailMultiAlternatives

load_dotenv()


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    context = {
        'current_user': reset_password_token.user,
        'fullname': reset_password_token.user.get_full_name(),
        'email': reset_password_token.user.email,
        'reset_password_url': "{}?token={}".format(reverse('password_reset:reset-password-request'),
                                                   reset_password_token.key)
    }

    email_plaintext_message = context

    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title="CleanStock Account"),
        # message:
        email_plaintext_message,
        # from:
        os.getenv("DEFAULT_FROM_EMAIL"),
        # to:
        [reset_password_token.user.email]
    )

    msg.send(fail_silently=True)


'''

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_access_token(sender, instance=None, created=False, **kwargs):
    if created:
        AccessToken.objects.create(expires=datetime.now() + timedelta(minutes=10), user=instance)
        RefreshToken.objects.create(user=instance)
'''
