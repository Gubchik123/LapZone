from django.urls import path

from . import views


app_name = "order"
urlpatterns = [
    path("<uuid:pk>/", views.OrderDetailView.as_view(), name="detail"),
]
