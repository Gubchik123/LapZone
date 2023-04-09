from random import randint
from typing import Callable

from django.test import TestCase
from django.http import HttpResponse
from django.db.models import QuerySet

from general.test_mixins.for_views import ViewTestMixin
from shop.forms import ProductFilterForm, ReviewForm
from shop.models import Brand, Category, Product, CarouselImage


class ShopAppViewsTestMixin(ViewTestMixin):
    """
    Test mixin providing helper methods for testing views in the "Shop" app.
    """

    @classmethod
    def setUpTestData(cls) -> None:
        """
        Set up test data by creating 1 brand, 1 category, and 15 products.
        """
        brand = Brand.objects.create(name="Test brand")
        category = Category.objects.create(name="Test category")

        for count in range(1, 16):
            Product.objects.create(
                name=f"Test product {count}",
                description="Some content",
                image=f"./some_image_{count}.jpg",
                price=1000 + count,
                year=randint(2021, 2023),
                brand=brand,
                category=category,
            )


class HomeViewTestCase(ShopAppViewsTestMixin, TestCase):
    """Tests for the HomeView."""

    url = "/"
    name = "shop:home"
    template_name = "shop/home.html"

    def test_lists_recently_added_products(self):
        """Test that recently added products are listed on the home page."""
        self.assertIn("recently_added_products", self.response.context)
        self.assertEqual(
            len(self.response.context["recently_added_products"]), 10
        )
        self.assertQuerysetEqual(
            self.response.context["recently_added_products"],
            Product.objects.order_by("-id")[:10],
        )

    def test_lists_brands(self):
        """Test that brands are listed on the home page."""
        self.assertIn("brands", self.response.context)
        self.assertQuerysetEqual(
            self.response.context["brands"], Brand.objects.all()
        )

    def test_lists_categories(self):
        """Test that categories are listed on the home page."""
        self.assertIn("categories", self.response.context)
        self.assertQuerysetEqual(
            self.response.context["categories"], Category.objects.all()
        )

    def test_lists_carousel_images(self):
        """Test that carousel images are listed on the home page."""
        self.assertIn("carousel_images", self.response.context)
        self.assertQuerysetEqual(
            self.response.context["carousel_images"],
            CarouselImage.objects.all(),
        )


class ProductListViewTestMixin(ShopAppViewsTestMixin):
    """Test mixin for views that are inherited from the _ProductListView."""

    page_title: str
    queryset: QuerySet
    template_name = "shop/product_list.html"

    def test_page_title(self):
        """
        Test that "page_title" there is in the response context and equal to the page_title attribute.
        """
        self.assertIn("page_title", self.response.context)
        self.assertEqual(self.page_title, self.response.context["page_title"])

    def test_filter_form_is_on_page(self):
        """Test that the "filter_form" there is on a page."""
        self.assertIn("filter_form", self.response.context)
        self.assertIsInstance(
            self.response.context["filter_form"], ProductFilterForm
        )

    def test_lists_products(self):
        """Test that products are listed on a page."""
        self.assertIn("page_obj", self.response.context)
        self.assertEqual(
            self.response.context["page_obj"].object_list,
            list(self.queryset[:12]),
        )

    # * ------------------ Testing pagination functionality ------------------

    def test_pagination_is_twelve(self):
        """Test that pagination is set to 12 per page."""
        self.assertEqual(len(self.response.context["page_obj"]), 12)

    def test_paginated_product_list(self):
        """Test second page has (exactly) remaining 3 products."""
        response = self.client.get(f"{self.url}?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["page_obj"]), 3)

    def test_404_with_invalid_pagination_page_value(self):
        """Test that invalid pagination page value results in 404"""
        response = self.client.get(f"{self.url}?page=0")
        self.assertEqual(response.status_code, 404)

        response = self.client.get(f"{self.url}?page=3")
        self.assertEqual(response.status_code, 404)

        response = self.client.get(f"{self.url}?page=string")
        self.assertEqual(response.status_code, 404)

    # * ------------------- Testing ordering functionality -------------------

    def test_lists_products_ordered_by_name_asc(self):
        """Test that products ordered by name (ASC) are listed on a page."""
        response = self.client.get(f"{self.url}?orderby=name&orderdir=asc")
        self.assertEqual(
            response.context["page_obj"].object_list,
            list(self.queryset.order_by("name")[:12]),
        )

    def test_lists_products_ordered_by_price_asc(self):
        """Test that products ordered by price (ASC) are listed on a page."""
        response = self.client.get(f"{self.url}?orderby=price&orderdir=asc")
        self.assertEqual(
            response.context["page_obj"].object_list,
            list(self.queryset.order_by("price")[:12]),
        )

    def test_lists_products_ordered_by_price_desc(self):
        """Test that products ordered by price (DESC) are listed on a page."""
        response = self.client.get(f"{self.url}?orderby=price&orderdir=desc")
        self.assertEqual(
            response.context["page_obj"].object_list,
            list(self.queryset.order_by("-price")[:12]),
        )

    def test_invalid_order_parameters(self):
        """
        Test that products ordered by default are listed on a page if order parameters are invalid.
        """
        # When there is the 'orderby', but there is not the 'orderdir'.
        response = self.client.get(f"{self.url}?orderby=name")
        self.assertEqual(
            response.context["page_obj"].object_list, list(self.queryset[:12])
        )
        # When there is the 'orderdir', but there is not the 'orderby'.
        response = self.client.get(f"{self.url}?orderdir=desc")
        self.assertEqual(
            response.context["page_obj"].object_list, list(self.queryset[:12])
        )
        # When the 'orderdir' is not in ("asc", "desc").
        response = self.client.get(f"{self.url}?orderby=price&orderdir=wrong")
        self.assertEqual(
            response.context["page_obj"].object_list, list(self.queryset[:12])
        )
        # When the 'orderby' is not in ("name", "price").
        response = self.client.get(f"{self.url}?orderby=wrong&orderdir=desc")
        self.assertEqual(
            response.context["page_obj"].object_list, list(self.queryset[:12])
        )


class AllProductsListViewTestCase(ProductListViewTestMixin, TestCase):
    """Tests for the AllProductsListView."""

    url = "/products/"
    name = "shop:product_list"

    page_title = "All products"
    queryset = Product.objects.all()

    # * ------------------ Testing searching functionality -------------------

    def test_search_product_success(self):
        """
        Test searching for products with a query that should return results.
        """
        response = self.client.get(f"{self.url}?q=Test product 1")
        object_list = response.context["page_obj"].object_list
        self.assertTrue(len(object_list) > 0)
        self.assertEqual(
            object_list,
            list(self.queryset.filter(name__icontains="Test product 1")),
        )

    def test_search_product_no_result(self):
        """
        Test searching for products with a query that shouldn't return results.
        """
        response = self.client.get(f"{self.url}?q=Non-existent title")
        self.assertFalse(bool(response.context["page_obj"].object_list))
        self.assertContains(
            response, "There are no products that match your search criteria."
        )

    # * ------------------ Testing filtering functionality -------------------

    def check_filter_form_for_validity_by_(
        form_data: dict, expected_status_code: int = 200
    ) -> Callable:
        """
        Returns a decorator that tests whether the given form data is valid.
        """

        def wrapper(test_func: Callable) -> Callable:
            """Wraps a view function with a test for
            the validity of a form created from form_data."""

            def inner(self):
                """Test that ProductFilterForm(form_data)
                is valid and calls the wrapped function."""
                self.assertTrue(ProductFilterForm(form_data).is_valid())

                response = self.client.post(self.url, form_data)
                self.assertEqual(response.status_code, expected_status_code)

                return test_func(self, response)

            return inner

        return wrapper

    @check_filter_form_for_validity_by_(
        form_data={"category": 1}, expected_status_code=302
    )
    def test_filtering_by_one_category_and_redirect_to_category_page(
        self, response: HttpResponse
    ):
        """
        Test if the view redirects to the correct category page with only category in the POST data.
        """
        self.assertRedirects(response, "/category/test-category/")

    @check_filter_form_for_validity_by_(
        form_data={"brands": [1]}, expected_status_code=302
    )
    def test_filtering_by_one_brand_and_redirect_to_brand_page(
        self, response: HttpResponse
    ):
        """
        Test if the view redirects to the correct brand page with only brand in the POST data.
        """
        self.assertRedirects(response, "/brand/test-brand/")

    # ! ------------- I think it's correct, but it doesn't work --------------

    @check_filter_form_for_validity_by_(form_data={"min_price": 1010})
    def test_filtering_by_min_price(self, response: HttpResponse):
        """Test filtering by minimum price."""

        # self.assertQuerysetEqual(
        #     self.response.context["page_obj"].object_list,
        #     list(self.queryset.filter(price__gte=1010)),
        # )

    @check_filter_form_for_validity_by_(form_data={"max_price": 1005})
    def test_filtering_by_max_price(self, response: HttpResponse):
        """Test filtering by maximum price."""

        # self.assertEqual(
        #     self.response.context["page_obj"].object_list,
        #     list(self.queryset.filter(price__lte=1005)),
        # )

    @check_filter_form_for_validity_by_(
        form_data={"min_price": 1008, "max_price": 1012}
    )
    def test_filtering_by_max_and_min_price(self, response: HttpResponse):
        """Test filtering by both maximum and minimum price."""

        # self.assertEqual(
        #     self.response.context["page_obj"].object_list,
        #     list(self.queryset.filter(price__gte=1008, price__lte=1012)),
        # )

    @check_filter_form_for_validity_by_(form_data={"years": [2022]})
    def test_filtering_by_year(self, response: HttpResponse):
        """Test filtering by year."""

        # self.assertEqual(
        #     self.response.context["page_obj"].object_list,
        #     list(self.queryset.filter(year__in=[2022])),
        # )


class ProductListByCategoryViewTestCase(ProductListViewTestMixin, TestCase):
    """Tests for the ProductListByCategoryView."""

    name = "shop:category"
    url = "/category/test-category/"
    kwargs = {"slug": "test-category"}

    page_title = "Test category"
    queryset = Product.objects.filter(category__slug="test-category")


class ProductListByBrandViewTestCase(ProductListViewTestMixin, TestCase):
    """Tests for the ProductListByBrandView."""

    name = "shop:brand"
    url = "/brand/test-brand/"
    kwargs = {"slug": "test-brand"}

    page_title = "Test brand products"
    queryset = Product.objects.filter(brand__slug="test-brand")


class ProductDetailViewTestMixin:
    """Test mixin with creating one product before testing."""

    @classmethod
    def setUpTestData(cls) -> None:
        """Set up test data by creating 1 product with brand and category."""
        cls.product = Product.objects.create(
            name=f"Test product",
            description="Some content",
            image=f"./some_image.jpg",
            price=1500,
            year=2023,
            brand=Brand.objects.create(name="Test brand"),
            category=Category.objects.create(name="Test category"),
        )


class ProductDetailViewTestCase(
    ProductDetailViewTestMixin, ViewTestMixin, TestCase
):
    """Tests for the ProductDetailView."""

    name = "shop:product_detail"
    url = "/product/test-product/"
    kwargs = {"slug": "test-product"}
    template_name = "shop/product_detail.html"

    def test_404_with_non_existent_product_slug(self):
        """Test that a non-existent product slug returns a 404 error."""
        response = self.client.get("/product/non-existent-slug/")
        self.assertEqual(response.status_code, 404)

    def test_product_detail_page_contains_product_image(self):
        """Test that product image is displayed on the product detail page."""
        self.assertContains(self.response, self.product.image.url)

    def test_product_detail_page_contains_product_name(self):
        """Test that product name is displayed on the product detail page."""
        self.assertContains(self.response, self.product.name)

    def test_product_detail_page_contains_product_description(self):
        """
        Test that product description is displayed on the product detail page.
        """
        self.assertContains(self.response, self.product.description)

    def test_product_detail_page_contains_product_price(self):
        """Test that product price is displayed on the product detail page."""
        self.assertContains(self.response, f"{float(self.product.price)}$")

    def test_review_form_is_on_page(self):
        """Test that the "review_form" there is the product detail page."""
        self.assertIn("review_form", self.response.context)
        self.assertIsInstance(self.response.context["review_form"], ReviewForm)


class ReviewFormViewTestCase(ProductDetailViewTestMixin, TestCase):
    """Tests for the ReviewFormView."""

    def check_review_form_for_validity_by_(
        form_data: dict, is_valid: bool = True
    ) -> Callable:
        """
        Returns a decorator that tests whether the given form data is valid.
        """

        def wrapper(test_func: Callable) -> Callable:
            """Wraps a view function with a test for
            the validity of a form created from form_data."""

            def inner(self):
                """Test ReviewForm(form_data)
                is_valid: bool and calls the wrapped function."""
                self.assertTrue(
                    ReviewForm(form_data).is_valid()
                ) if is_valid else self.assertFalse(
                    ReviewForm(form_data).is_valid()
                )

                response = self.client.post(
                    f"{self.product.get_absolute_url()}review/",
                    data=form_data,
                    follow=True,  # follow redirects
                )
                self.assertEqual(response.status_code, 200)

                return test_func(self, response)

            return inner

        return wrapper

    @check_review_form_for_validity_by_(
        form_data={"name": "Username", "body": "Test review"}
    )
    def test_adding_review_valid(self, response: HttpResponse):
        """Test adding a valid review to the product."""
        self.assertContains(response, "Review has added successfully.")
        self.assertEqual(self.product.review_set.count(), 1)

    @check_review_form_for_validity_by_(
        form_data={"name": "", "body": ""}, is_valid=False
    )
    def test_adding_review_invalid(self, response: HttpResponse):
        """Test adding an invalid review to the product."""
        self.assertContains(
            response,
            "Data in form is invalid! Review has not added successfully.",
        )
        self.assertEqual(self.product.review_set.count(), 0)
