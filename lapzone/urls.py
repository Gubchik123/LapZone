from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from . import views
from general.error_views import (
    CustomBadRequestView,
    CustomPermissionDeniedView,
    CustomNotFoundView,
)


handler400 = CustomBadRequestView.as_view()
handler403 = CustomPermissionDeniedView.as_view()
handler404 = CustomNotFoundView.as_view()

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("allauth.urls")),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path("", include("shop.urls")),
    path("cart/", include("cart.urls")),
    path("order/", include("order.urls")),
    path("profile/", include("customer.urls")),
    path("mailing/", include("mailing.urls")),
    path(
        "faq/",
        TemplateView.as_view(template_name="pages/FAQs.html"),
        name="faq",
    ),
    path(
        "about/",
        TemplateView.as_view(template_name="pages/about.html"),
        name="about",
    ),
    path(
        "feedback/",
        TemplateView.as_view(template_name="pages/feedback.html"),
        name="feedback",
    ),
    path("robots.txt", views.get_robots_txt, name="robots_txt"),
]
