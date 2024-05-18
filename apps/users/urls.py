from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("auth/", views.AuthView.as_view(), name="auth"),
    path("user-profile/", views.UserRetrieveAPIView.as_view(), name="user"),
]
