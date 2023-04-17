from django.urls import path

from . import views


app_name = "cart"
urlpatterns = [
    path("cart/", views.CartDetailView.as_view(), name="detail"),
    path(
        "product/<slug:slug>/add-to-cart/",
        views.CartAddView.as_view(),
        name="add",
    ),
    path(
        "product/<slug:slug>/remove-from-cart/",
        views.CartRemoveView.as_view(),
        name="remove",
    ),
]
