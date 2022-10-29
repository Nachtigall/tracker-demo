from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    path("details/", views.UserDetailsView.as_view(), name="user-details"),
    path("auth/", obtain_auth_token, name="auth"),
]
