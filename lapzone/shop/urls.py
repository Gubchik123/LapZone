from django.urls import path

from . import views


app_name = "shop"
urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("search/", views.SearchProductListView.as_view(), name="search"),
    path("products/", views.AllProductsListView.as_view(), name="products"),
    path(
        "category/<slug:slug>/",
        views.ProductListByCategoryView.as_view(),
        name="category",
    ),
    path(
        "brand/<slug:slug>/",
        views.ProductListByBrandView.as_view(),
        name="brand",
    ),
]
