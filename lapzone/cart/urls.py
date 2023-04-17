from django.urls import path

from . import views


app_name = "cart"
urlpatterns = [
    path("cart/", views.CartDetailView, name="detail"),
    path("product/<slug:slug>/add-to-cart/", views.CartAddView, name="add"),
]
