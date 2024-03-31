from django.urls import path

from . import views


app_name = "order"
urlpatterns = [
    path("list/", views.OrderListView.as_view(), name="list"),
    path("checkout/", views.OrderCheckoutFormView.as_view(), name="create"),
    path("<uuid:pk>/", views.OrderDetailView.as_view(), name="detail"),
    path("<uuid:pk>/delete/", views.OrderDeleteView.as_view(), name="delete"),
]
