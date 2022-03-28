from django.urls import path
from members.api import views

app_name = "members"

urlpatterns = [
    path('register/', views.MemberCreationView.as_view()),
    path('dashboard/', views.DashboardView.as_view()),
]
