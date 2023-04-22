from django.urls import path
from django.views.generic import TemplateView

from . import views


app_name = "cart"
urlpatterns = [
    path(
        "",
        TemplateView.as_view(template_name="cart/detail.html"),
        name="detail",
    ),
    path(
        "add/",
        views.CartAddView.as_view(),
        name="add",
    ),
    path("update/", views.CartUpdateView.as_view(), name="update"),
    path(
        "remove/",
        views.CartRemoveView.as_view(),
        name="remove",
    ),
]
