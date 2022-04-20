from django.urls import path
from members.api import views

app_name = "members"

urlpatterns = [
    path('register/', views.MemberCreationView.as_view()),
    path('settings/<int:pk>/', views.UpdateDataView.as_view()),
]
