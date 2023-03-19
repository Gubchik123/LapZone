from django.urls import path

from . import views


app_name = "shop"
urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path(
        "category/<slug:slug>/",
        views.CategoryDetailListView.as_view(),
        name="category",
    ),
    path(
        "brand/<slug:slug>/",
        views.BrandDetailListView.as_view(),
        name="brand",
    ),
]
