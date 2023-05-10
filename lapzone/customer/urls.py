from django.urls import path

from . import views

app_name = "customer"
urlpatterns = [
    path("", views.CustomerDetailView.as_view(), name="detail"),
]