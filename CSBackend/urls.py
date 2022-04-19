from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from CSBackend import views
from users.api import views as users_views

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

    # LOCAL API
    path('api/user/', include('users.api.urls')),
    path('api/member/', include('members.api.urls')),
    path('api/community/', include('communities.api.urls')),
    path('api/partner/', include('partners.api.urls')),
    path('api/nip/', views.CompanyNIP.as_view()),
    path('api/zip/', views.MapZIP.as_view()),

    # PASSWORD RESET
    path('api/user/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

    # REST FRAMEWORK
    path('api-auth/', include('rest_framework.urls')),

    # OAUTH2
    path('oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('oauth/token/login/', users_views.TokenView.as_view(), name="token"),

    # SWAGGER
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
