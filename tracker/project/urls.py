from django.urls import path

from . import views

urlpatterns = [
    path("", views.ProjectView.as_view(), name="project"),
    path("<int:pk>/", views.ProjectDetailsView.as_view(), name="project-details"),
]
