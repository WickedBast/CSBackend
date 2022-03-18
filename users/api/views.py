import jwt
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

import random
from django.conf import settings
from users.models import User

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from oauth2_provider.models import AccessToken, RefreshToken
from datetime import datetime, timedelta

from rest_framework.views import APIView
from rest_framework.generics import (
    CreateAPIView,
    GenericAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView
)
from users.api.serializers import (
    RegistrationSerializer,
    EmailVerificationSerializer,
    LoginSerializer,
    ChangePasswordSerializer,
    RegistrationPasswordSerializer,
)


class RegistrationView(CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = []
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            RefreshToken.objects.create(
                user=user, token="".join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(16)),
                revoked=datetime.now(), application_id=1,
            )
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
            }, status=status.HTTP_406_NOT_ACCEPTABLE)


class RegistrationPasswordView(UpdateAPIView):
    serializer_class = RegistrationPasswordSerializer
    permission_classes = []
    authentication_classes = []

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # confirm the new passwords match
            password = serializer.data.get("password")
            confirm_password = serializer.data.get("password2")
            if password != confirm_password:
                return Response({"password": ["Passwords must match"]}, status=status.HTTP_400_BAD_REQUEST)

            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("password"))
            self.request.user.is_active = True
            self.object.save()
            return Response({"response": "successfully changed password"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(CreateAPIView):
    serializer_class = LoginSerializer
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        context = {}

        email = request.POST.get('email')
        password = request.POST.get('password')
        account = authenticate(email=email, password=password)
        if account:
            try:
                token = AccessToken.objects.get(user=account)
            except AccessToken.DoesNotExist:
                token = AccessToken.objects.create(
                    user=account, expires=datetime.now() + timedelta(minutes=10),
                    token="".join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(16)),
                    application_id=1,
                )
            context['response'] = 'Successfully authenticated.'
            context['pk'] = account.pk
            context['email'] = email.lower()
            context['token'] = token.token
            return Response(context, status=status.HTTP_202_ACCEPTED)
        else:
            context['response'] = 'Error'
            context['error_message'] = 'Invalid credentials'
            return Response(context, status=status.HTTP_406_NOT_ACCEPTABLE)


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


class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


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
