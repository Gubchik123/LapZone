from django.urls import path

from . import views


app_name = "customer"
urlpatterns = [
    path("", views.CustomerDetailView.as_view(), name="detail"),
    path("wish-list/", views.CustomerWishListView.as_view(), name="wish_list"),
    path("update/", views.CustomerUpdateView.as_view(), name="update"),
    path("delete/", views.CustomerDeleteView.as_view(), name="delete"),
]
