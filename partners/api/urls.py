from django.urls import path
from partners.api import views

app_name = "partners"

urlpatterns = [
    path('register/', views.PartnerCreationView.as_view(), name="register")
]
