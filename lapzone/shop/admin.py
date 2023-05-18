from django import forms
from django.urls import reverse
from django.contrib import admin
from django.http import HttpRequest
from django.db.models import QuerySet
from django.utils.safestring import mark_safe, SafeText
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from . import models
from general.admin_mixins import (
    ModelWithPriceAdminMixin,
    ModelWithFKToProductAdminMixin,
    ModelWithFKToUserAdminMixin,
)


admin.site.site_title = admin.site.site_header = "LapZone Admin"


class BaseModelAdmin:
    """Base admin class with general options"""

    list_per_page = 25
    ordering = ("id",)


class ModelWithNameAdminMixin:
    """Admin mixin for managing instances
    that inherited from abstract ModelWithName"""

    search_fields = ("name",)
    search_help_text = "Searching by name"


class ModelWithNameAndSlugAdminMixin(ModelWithNameAdminMixin):
    """Admin mixin for managing instances that
    inherited from abstract ModelWithNameAndSlug"""

    prepopulated_fields = {"slug": ("name",)}


@admin.register(models.Brand)
class BrandModelAdmin(
    BaseModelAdmin, ModelWithNameAndSlugAdminMixin, admin.ModelAdmin
):
    """Admin class for managing Brand instances."""

    list_display_links = ("id", "name")
    list_display = ("id", "name", "slug")


@admin.register(models.Category)
class CategoryModelAdmin(
    BaseModelAdmin, ModelWithNameAndSlugAdminMixin, admin.ModelAdmin
):
    """Admin class for managing Category instances."""

    list_display_links = ("id", "name")
    list_display = ("id", "name", "slug")


class ModelWithImageAdminMixin:
    """Admin mixin for managing instances
    that inherited from abstract ModeWithImage"""

    def get_image(self, obj: models.Product | models.ProductShot) -> SafeText:
        """Returns HTML image tag with product or product shot image url"""
        return mark_safe(
            f"<img src='{obj.image.url}' width='60' height='60' />"
        )

    get_image.short_description = "Mini image"


class ProductAdminForm(forms.ModelForm):
    """
    Model form for adding 'ckeditor' uploading widget to 'description' field
    """

    description = forms.CharField(
        label="Description", widget=CKEditorUploadingWidget()
    )

    class Meta:
        model = models.Product
        fields = "__all__"


class ProductShotInline(ModelWithImageAdminMixin, admin.TabularInline):
    """Custom admin TabularInline for embedded product shots"""

    extra = 0
    max_num = 5
    model = models.ProductShot
    fields = ("name", "get_image")
    readonly_fields = ("get_image",)


@admin.register(models.Product)
class ProductModelAdmin(
    BaseModelAdmin,
    ModelWithNameAndSlugAdminMixin,
    ModelWithImageAdminMixin,
    ModelWithPriceAdminMixin,
    admin.ModelAdmin,
):
    """Admin class for managing Product instances."""

    save_on_top = True
    form = ProductAdminForm
    list_display_links = ("id", "name")
    list_filter = ("brand", "category", "year")
    readonly_fields = ("get_brand_link", "get_category_link", "get_image")
    list_display = (
        "id",
        "name",
        "get_price",
        "year",
        "get_brand_link",
        "get_category_link",
        "get_image",
    )
    fieldsets = (
        ("Header".upper(), {"fields": (("name", "slug"),)}),
        (
            "Content".upper(),
            {
                "fields": (
                    "description",
                    ("image", "get_image"),
                    ("price", "year"),
                    ("brand", "category"),
                )
            },
        ),
    )
    inlines = (ProductShotInline,)

    def get_brand_link(self, product: models.Product) -> SafeText:
        """Returns link to the admin page for product.brand"""
        link_to_brand = reverse(
            "admin:shop_brand_change", args=(product.brand.pk,)
        )
        return mark_safe(f"<a href='{link_to_brand}'>{product.brand.name}</a>")

    get_brand_link.short_description = "Brand"

    def get_category_link(self, product: models.Product) -> SafeText:
        """Returns link to the admin page for product.category"""
        link_to_category = reverse(
            "admin:shop_category_change", args=(product.category.pk,)
        )
        return mark_safe(
            f"<a href='{link_to_category}'>{product.category.name}</a>"
        )

    get_category_link.short_description = "Category"


@admin.register(models.ProductShot)
class ProductShotModelAdmin(
    BaseModelAdmin,
    ModelWithNameAdminMixin,
    ModelWithImageAdminMixin,
    ModelWithFKToProductAdminMixin,
    admin.ModelAdmin,
):
    """Admin class for managing ProductShot instances."""

    list_display_links = ("id", "name")
    readonly_fields = ("get_product_link", "get_image")
    list_display = ("id", "name", "get_product_link", "get_image")
    fields = ("name", "description", "product", ("image", "get_image"))


@admin.register(models.Like)
class LikeModelAdmin(
    BaseModelAdmin,
    ModelWithFKToProductAdminMixin,
    ModelWithFKToUserAdminMixin,
    admin.ModelAdmin,
):
    """Admin class for managing Like instances."""

    search_fields = ("product__name",)
    search_help_text = "Searching by product"
    list_filter = ("product", "user__username")
    readonly_fields = ("get_product_link", "get_user_link")
    list_display = ("id", "get_user_link", "get_product_link", "created")
    fields = (("product", "get_product_link"), ("user", "get_user_link"))


class ReviewParentListFilter(admin.SimpleListFilter):
    """Custom list filter by review parent"""

    title = "Parent review"
    parameter_name = "parent"

    def lookups(
        self, request: HttpRequest, model_admin: models.Review
    ) -> tuple[tuple[str, str]]:
        """Returns variants of filtering"""
        return (("Yes", "There is"), ("No", "There is not"))

    def queryset(self, request: HttpRequest, queryset: QuerySet) -> QuerySet:
        """Compares the requested value (either 'Yes' or 'No')
        to decide how to filter the queryset."""
        if self.value() == "Yes":
            return queryset.filter(parent__isnull=False)
        elif self.value() == "No":
            return queryset.filter(parent__isnull=True)


@admin.register(models.Review)
class ReviewModelAdmin(
    BaseModelAdmin, ModelWithFKToProductAdminMixin, admin.ModelAdmin
):
    """Admin class for managing Review instances."""

    search_help_text = "Searching by username"
    list_filter = ("product", "name", ReviewParentListFilter)
    readonly_fields = (
        "name",
        "created",
        "get_product_link",
        "get_parent_link",
    )
    list_display = (
        "id",
        "name",
        "get_parent_link",
        "get_product_link",
        "created",
    )
    fields = (
        ("product", "get_product_link"),
        "name",
        "body",
        ("parent", "get_parent_link"),
        "created",
    )

    def get_parent_link(self, review: models.Review) -> SafeText | str:
        """
        Returns link to the admin page for parent review if this one has it
        """
        if review.parent:
            link_to_user = reverse(
                "admin:shop_review_change", args=(review.parent.pk,)
            )
            return mark_safe(
                f"<a href='{link_to_user}'>{str(review.parent)}</a>"
            )
        return "-"

    get_parent_link.short_description = "Parent review"


@admin.register(models.CarouselImage)
class CarouselImageModelAdmin(
    BaseModelAdmin,
    ModelWithNameAdminMixin,
    ModelWithImageAdminMixin,
    ModelWithFKToProductAdminMixin,
    admin.ModelAdmin,
):
    """Admin class for managing CarouselImage instances."""

    list_display_links = ("id", "name")
    readonly_fields = ("get_image", "get_product_link")
    list_display = ("id", "name", "get_product_link", "get_image")
    fields = (
        "name",
        "description",
        ("image", "get_image"),
        ("product", "get_product_link"),
    )
