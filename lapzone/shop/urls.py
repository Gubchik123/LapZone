from django.urls import path

from . import views


app_name = "shop"
urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path(
        "products/", views.AllProductsListView.as_view(), name="product_list"
    ),
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
    path(
        "product/<slug:slug>/",
        views.ProductDetailView.as_view(),
        name="product_detail",
    ),
    path(
        "product/<slug:slug>/review/",
        views.ReviewFormView.as_view(),
        name="add_review_to_product",
    ),
]
