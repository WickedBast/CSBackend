from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

schema_view = get_schema_view(
    openapi.Info(
        title="Clean Stock API",
        default_version='v1',
        description="Clean Stock",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@vivadrive.io"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # USER API
    path('api/user/', include('users.api.urls')),
    path('api/user/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

    # REST FRAMEWORK
    path('api-auth/', include('rest_framework.urls')),

    # OAUTH2
    # path('oauth2/', include('provider.oauth2.urls', namespace='oauth2')),

    # JWT TOKEN
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # SWAGGER
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
