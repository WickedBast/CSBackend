from django.urls import path
from communities.api import views

app_name = "communities"

urlpatterns = [
    path('register/', views.CommunityCreationView.as_view())
]
