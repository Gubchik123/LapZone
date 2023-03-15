from django.db import models

from shop.models import Product


class ModelMetaOptionsTestMixin:
    """Mixin for testing the base meta options of models."""

    model: models.Model
    verbose_name: str
    verbose_name_plural: str
    ordering: list[str]

    def test_model_verbose_name(self):
        """
        Test that the model's verbose name is equal to the verbose_name attribute.
        """
        self.assertEqual(self.model._meta.verbose_name, self.verbose_name)

    def test_model_verbose_name_plural(self):
        """
        Test that the model's verbose name (plural) is equal to the verbose_name_plural attribute.
        """
        self.assertEqual(
            self.model._meta.verbose_name_plural, self.verbose_name_plural
        )

    def test_model_fields_ordering(self):
        """
        Test that the model's ordering is equal to the ordering attribute.
        """
        self.assertEqual(self.model._meta.ordering, self.ordering)


class ModelWithNameTestMixin:
    """Mixin for testing the 'name' field parameters
    for models that inherited from abstract ModelWithNameTest."""

    model: models.Model
    # Default parameter values.
    name_blank = False
    name_unique = True
    name_max_length = 100
    name_verbose_name = "Name"

    def test_model_string_representation(self):
        """Test the model string representation by __str__."""
        obj = self.model.objects.get(id=1)
        self.assertEqual(str(obj), obj.name)

    def test_name_verbose_name(self):
        """
        Test that the name field's verbose name is equal to the name_verbose_name attribute.
        """
        self.assertEqual(
            self.model._meta.get_field("name").verbose_name,
            self.name_verbose_name,
        )

    def test_name_max_length(self):
        """
        Test that the name field's max length is equal to the name_max_length attribute.
        """
        self.assertEqual(
            self.model._meta.get_field("name").max_length, self.name_max_length
        )

    def test_name_unique(self):
        """
        Test that the name field's unique is equal to the name_unique attribute.
        """
        self.assertEqual(
            self.model._meta.get_field("name").unique, self.name_unique
        )

    def test_name_blank(self):
        """
        Test that the name field's blank is equal to the name_blank attribute.
        """
        self.assertEqual(
            self.model._meta.get_field("name").blank, self.name_blank
        )


class ModelWithNameAndSlugTestMixin(ModelWithNameTestMixin):
    """Mixin for testing the 'name' and 'slug' fields parameters
    for models that inherited from abstract ModelWithNameAndSlug."""

    # Default parameter values.
    slug_blank = False
    slug_unique = True
    slug_max_length = 100
    slug_verbose_name = "Slug"

    expected_slug: str
    
    def test_slug_generating(self):
        """Test that the slug was generated correctly"""
        obj: models.Model = self.model.objects.get(id=1)
        self.assertEqual(obj.slug, self.expected_slug)

    def test_slug_verbose_name(self):
        """
        Test that the slug field's verbose name is equal to the slug_verbose_name attribute.
        """
        self.assertEqual(
            self.model._meta.get_field("slug").verbose_name,
            self.slug_verbose_name,
        )

    def test_slug_max_length(self):
        """
        Test that the slug field's max length is equal to the slug_max_length attribute.
        """
        self.assertEqual(
            self.model._meta.get_field("slug").max_length, self.slug_max_length
        )

    def test_slug_unique(self):
        """
        Test that the slug field's unique is equal to the slug_unique attribute.
        """
        self.assertEqual(
            self.model._meta.get_field("slug").unique, self.slug_unique
        )

    def test_slug_blank(self):
        """
        Test that the slug field's blank is equal to the slug_blank attribute.
        """
        self.assertEqual(
            self.model._meta.get_field("slug").blank, self.slug_blank
        )


class ModelWithDescriptionTestMixin:
    """Mixin for testing the 'description' field parameters
    for models that inherited from abstract ModelWithDescription."""

    # Default parameter values.
    description_blank = False
    description_verbose_name = "Description"

    def test_description_verbose_name(self):
        """
        Test that the description field's verbose name is equal to the description_verbose_name attribute.
        """
        self.assertEqual(
            self.model._meta.get_field("description").verbose_name,
            self.description_verbose_name,
        )

    def test_description_blank(self):
        """
        Test that the description field's blank is equal to the description_blank attribute.
        """
        self.assertEqual(
            self.model._meta.get_field("description").blank,
            self.description_blank,
        )


class ModelWithImageTestMixin:
    """Mixin for testing the 'image' field parameters
    for models that inherited from abstract ModelWithImageTestMixin."""

    # Default parameter values.
    image_blank = False
    image_upload_to: str
    image_verbose_name = "Image"

    def test_image_verbose_name(self):
        """
        Test that the image field's verbose name is equal to the image_verbose_name attribute.
        """
        self.assertEqual(
            self.model._meta.get_field("image").verbose_name,
            self.image_verbose_name,
        )

    def test_image_blank(self):
        """
        Test that the image field's blank is equal to the image_blank attribute.
        """
        self.assertEqual(
            self.model._meta.get_field("image").blank,
            self.image_blank,
        )

    def test_image_upload_path(self):
        """
        Test that the image field's upload path is equal to the image_upload_to attribute.
        """
        self.assertEqual(
            self.model._meta.get_field("image").upload_to,
            self.image_upload_to,
        )


class ModelWithCreatedDateTimeTestMixin:
    """Mixin for testing the 'created' field parameters
    for models that inherited from abstract ModelWithCreatedDateTime."""

    # Default parameter values.
    created_auto_now_add = True
    created_verbose_name = "Created at"

    def test_created_verbose_name(self):
        """
        Test that the created field's verbose name is equal to the created_verbose_name attribute.
        """
        self.assertEqual(
            self.model._meta.get_field("created").verbose_name,
            self.created_verbose_name,
        )

    def test_created_auto_now_add(self):
        """
        Test that the created field's auto_now_add is equal to the created_auto_now_add attribute.
        """
        self.assertEqual(
            self.model._meta.get_field("created").auto_now_add,
            self.created_auto_now_add,
        )


class ModelWithFKToProductTestMixin:
    """Mixin for testing the 'product' field parameters
    for models that inherited from abstract ModelWithFKToProduct."""

    # Default parameter values.
    product_related_model = Product
    # product_on_delete = models.CASCADE
    product_verbose_name = "For product"

    def test_product_verbose_name(self):
        """
        Test that the product field's verbose name is equal to the product_verbose_name attribute.
        """
        self.assertEqual(
            self.model._meta.get_field("product").verbose_name,
            self.product_verbose_name,
        )

    # def test_product_on_delete(self):
    #     """
    #     Test that the product field's on_delete is equal to the product_on_delete attribute.
    #     """
    #     self.assertEqual(
    #         self.model._meta.get_field("product").on_delete,
    #         self.product_on_delete,
    #     )

    def test_product_related_model(self):
        """
        Test that the product field's related model is equal to the product_related_model attribute.
        """
        self.assertEqual(
            self.model._meta.get_field("product").related_model,
            self.product_related_model,
        )
