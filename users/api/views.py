import json
import os

import jwt
import requests
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.debug import sensitive_post_parameters
from django_rest_passwordreset import models
from django_rest_passwordreset.models import ResetPasswordToken
from django_rest_passwordreset.views import ResetPasswordRequestToken
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from oauth2_provider.views.base import TokenView as OAuth2TokenView
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from communities.models import CommunityUsers
from members.models import Member, MemberUsers
from partners.models import PartnerUsers
from users.api.serializers import (
    RegistrationSerializer,
    EmailVerificationSerializer,
    ChangePasswordSerializer,
    RegistrationPasswordSerializer,
)
from users.models import User


class RegistrationView(CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = []
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({
                "response": "User Successfully Created.",
                "email": user.email,
                "pk": user.pk,
                "type": user.types,
                "created": user.date_joined,
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "response": "Something went wrong!"
            }, status=status.HTTP_400_BAD_REQUEST)


class RegistrationPasswordView(CreateAPIView):
    serializer_class = RegistrationPasswordSerializer
    permission_classes = []
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
        except (KeyError, ValueError, AttributeError):
            return Response({"data": ["Data is invalid"]}, status=status.HTTP_400_BAD_REQUEST)

        password = data.get('newPassword')
        token_value = data.get('token')

        if not password:
            return Response({"password": ["Password is empty"]}, status=status.HTTP_400_BAD_REQUEST)

        if not token_value:
            return Response({"token": ["Token is empty"]}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = models.ResetPasswordToken.objects.get(key=token_value)
        except models.ResetPasswordToken.DoesNotExist:
            return Response({"token": ["Token is invalid or expired"]}, status=status.HTTP_400_BAD_REQUEST)

        token.user.set_password(password)
        token.user.is_active = True
        token.user.save()

        token.delete()
        return Response({"response": "successfully created the password"}, status=status.HTTP_200_OK)


class VerifyEmailView(APIView):
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY, description='Description',
                                           type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            user = User.objects.get(id=payload['user_id'])
            if not user.is_active:
                user.is_active = True
                user.save()

            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)

        except jwt.exceptions.DecodeError:
            return Response({'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

            # confirm the new passwords match
            new_password = serializer.data.get("new_password")
            confirm_new_password = serializer.data.get("confirm_new_password")
            if new_password != confirm_new_password:
                return Response({"new_password": ["New passwords must match"]}, status=status.HTTP_400_BAD_REQUEST)

            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({"response": "successfully changed password"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(ResetPasswordRequestToken):
    permission_classes = []
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        resp = super().post(request=request, *args, **kwargs)

        if resp.status_code == 200:
            current_site = get_current_site(request=request).domain

            reset_password_token = ResetPasswordToken.objects.get(
                user=User.objects.get(email=request.data.get("email")))

            try:
                requests.post(
                    "https://api.eu.mailgun.net/v3/cleanstock.eu/messages",
                    auth=("api", os.getenv("MAILGUN_API_KEY")),
                    data={"from": "Clean Stock Team <noreply@cleanstock.eu>",
                          "to": reset_password_token.user.email,
                          "subject": "Password Reset for Clean Stock Account",
                          "template": "reset_password",
                          "v:domain": "localhost:3000",
                          "v:reset_password_url": "{}?token={}".format(
                              "/reset-password/",
                              reset_password_token.key),
                          }
                )
                return Response({'email': 'Email sent successfully'}, status=status.HTTP_200_OK)
            except:
                return Response({'error': 'Email Failed'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(self.serializer_class.errors)


@method_decorator(csrf_exempt, name="dispatch")
class TokenView(OAuth2TokenView):

    @method_decorator(sensitive_post_parameters("password"))
    def post(self, request, *args, **kwargs):
        try:
            u = User.objects.get(email=request.POST['username'])
            if not u.is_active:
                return JsonResponse(
                    status=403,
                    data={"message": _("Invalid credentials given.")},
                    safe=False
                )
            if not u.is_staff or not u.is_superuser:
                is_member = MemberUsers.objects.filter(users=u).exists()
                is_community = CommunityUsers.objects.filter(users=u).exists()
                is_partner = PartnerUsers.objects.filter(users=u).exists()

                if not is_member and not is_community and not is_partner:
                    return JsonResponse(
                        status=403,
                        data={"message": _("Invalid credentials given.")},
                        safe=False
                    )
        except:
            return JsonResponse(
                status=403,
                data={"message": _("Invalid credentials given.")},
                safe=False
            )

        response = super().post(request, args, kwargs)

        if response.status_code == 200:
            d = json.loads(response.content.decode('utf8'))

            if MemberUsers.objects.filter(users=u).exists():
                member_user = MemberUsers.objects.get(users=u)

                if isinstance(member_user, MemberUsers):
                    try:  # INDIVIDUAL
                        member_user.member.get_full_name()
                        if member_user.member.type == Member.Types.PROSPECT.name:
                            d['role'] = "Prospect"
                        elif member_user.member.type == Member.Types.SCHOOL.name:
                            d['role'] = "School"
                        elif member_user.member.type == Member.Types.PROSUMENT.name:
                            d['role'] = "Prosumer"
                        elif member_user.member.type == Member.Types.BENEFICIARY.name:
                            d['role'] = "Beneficiary"
                    except:  # ORGANIZATION
                        d['role'] = "OrganizationsCooperatives"

            elif PartnerUsers.objects.filter(users=u).exists():
                partner_user = PartnerUsers.objects.get(users=u)

                if isinstance(partner_user, PartnerUsers):
                    d['role'] = "Partner"

            elif u.is_superuser and u.is_staff:
                d['role'] = "Admin"

            else:
                return JsonResponse(
                    status=403,
                    data={"message": _("Invalid credentials given.")},
                    safe=False
                )

            response.content = json.dumps(d)

        return response
