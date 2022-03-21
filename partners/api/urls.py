from django.urls import path
from partners.api import views

app_name = "partners"

urlpatterns = [
    path('nip/<nip>/', views.FleetNip.as_view()),
]
