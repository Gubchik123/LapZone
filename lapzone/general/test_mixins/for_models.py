from django.db.models import Model
from django.contrib.auth.models import User

from shop.models import Product


class ModelTestMixin:
    """Base mixin with general methods."""

    def _get_first_model(self) -> Model:
        """Returns the first model depending on self.model"""

        # * Workaround to avoid the DoesNotExist during ProductModelTest
        try:
            return self.model.objects.get(id=1)
        except self.model.DoesNotExist:
            return self.model.objects.get(name="Test laptop")


class ModelMetaOptionsTestMixin:
    """Mixin for testing the base meta options of models."""

    model: Model
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


class ModelWithNameTestMixin(ModelTestMixin):
    """Mixin for testing the 'name' field parameters
    for models that inherited from abstract ModelWithNameTest."""

    # Default parameter values.
    name_blank = False
    name_unique = True
    name_max_length = 100
    name_verbose_name = "Name"

    def test_model_string_representation(self):
        """Test the model string representation by __str__."""
        obj = self._get_first_model()
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
    slug_blank = True
    slug_unique = True
    slug_max_length = 100
    slug_verbose_name = "Slug"

    url_pattern_name: str

    expected_url: str
    expected_slug: str

    def test_slug_generating(self):
        """Test that the slug was generated correctly"""
        obj = self._get_first_model()
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

    def test_url_pattern_name(self):
        """
        Test that the instance's url_pattern_name is equal to the url_pattern_name attribute.
        """
        obj: Model = self._get_first_model()
        self.assertEqual(obj.url_pattern_name, self.url_pattern_name)

    def test_get_absolute_url(self):
        """
        Test that the instance's get_absolute_url is equal to the expected_url attribute.
        """
        obj: Model = self._get_first_model()
        self.assertEqual(obj.get_absolute_url(), self.expected_url)


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


class ModelWithImageTestMixin(ModelTestMixin):
    """Mixin for testing the 'image' field parameters
    for models that inherited from abstract ModelWithImage."""

    # Default parameter values.
    image_blank = False
    image_upload_to: str
    image_verbose_name = "Image"

    expected_image_name: str

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

    def test_generated_image_name(self):
        """
        Test that the instance's image name is equal to the expected_image_name attribute.
        """
        self.assertEqual(
            self._get_first_model().image.name, self.expected_image_name
        )


class ModelWithPriceTestMixin(ModelTestMixin):
    """Mixin for testing the 'price' field parameters
    for models that inherited from abstract ModelWithPrice."""

    # Default parameter values.
    price_blank = False
    price_verbose_name = "Price"

    def test_price_blank(self):
        """
        Test that the price field's blank is equal to the price_blank attribute.
        """
        self.assertEqual(self.model._meta.get_field("price").blank, False)

    def test_price_verbose_name(self):
        """
        Test that the price field's verbose name is equal to the price_verbose_name attribute.
        """
        self.assertEqual(
            self.model._meta.get_field("price").verbose_name, "Price"
        )


class ModelWithCreatedDateTimeTestMixin:
    """Mixin for testing the 'created' field parameters
    for models that inherited from abstract ModelWithCreatedDateTime."""

    # Default parameter values.
    created_auto_now_add = True
    created_verbose_name = "Created datetime"

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
    product_verbose_name = "Product"

    def test_product_verbose_name(self):
        """
        Test that the product field's verbose name is equal to the product_verbose_name attribute.
        """
        self.assertEqual(
            self.model._meta.get_field("product").verbose_name,
            self.product_verbose_name,
        )

    def test_product_related_model(self):
        """
        Test that the product field's related model is equal to the product_related_model attribute.
        """
        self.assertEqual(
            self.model._meta.get_field("product").related_model,
            self.product_related_model,
        )

    def test_product_on_delete_cascade(self):
        """Test that the product field's on_delete is CASCADE."""
        Product.objects.get(name="Test laptop").delete()
        with self.assertRaises(self.model.DoesNotExist):
            self.model.objects.get(id=1)


class ModelWithFKToUserTestMixin:
    """Mixin for testing the 'user' field parameters
    for models that inherited from abstract ModelWithFKToUser."""

    # Default parameter values.
    user_related_model = User
    user_verbose_name = "User"

    def test_user_verbose_name(self):
        """
        Test that the user field's verbose name is equal to the user_verbose_name attribute.
        """
        self.assertEqual(
            self.model._meta.get_field("user").verbose_name,
            self.user_verbose_name,
        )

    def test_user_related_model(self):
        """
        Test that the user field's related model is equal to the user_related_model attribute.
        """
        self.assertEqual(
            self.model._meta.get_field("user").related_model,
            self.user_related_model,
        )

    def test_user_on_delete_cascade(self):
        """Test that the user field's on_delete is CASCADE."""
        User.objects.get(id=1).delete()
        with self.assertRaises(self.model.DoesNotExist):
            self.model.objects.get(id=1)
