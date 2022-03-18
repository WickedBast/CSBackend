from django.urls import path
from members.api import views

app_name = "members"

urlpatterns = [
    path('nip/<nip>/', views.FleetNip.as_view()),
]
