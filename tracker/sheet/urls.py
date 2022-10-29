from django.urls import path

from . import views

urlpatterns = [
    path("", views.SheetView.as_view(), name="sheet"),
    path("<int:pk>/", views.SheetDetailsView.as_view(), name="sheet-details"),
]
