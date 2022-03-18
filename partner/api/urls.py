from django.urls import path
from partner.api import views

app_name = "partner"

urlpatterns = [
    path('nip/<nip>/', views.FleetNip.as_view()),
]
