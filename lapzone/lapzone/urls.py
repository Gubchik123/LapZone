from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.views.generic import TemplateView

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
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
