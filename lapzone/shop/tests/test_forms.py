from django import forms
from django.test import TestCase

from shop.models import Category, Brand, Review
from shop.forms import ProductFilterForm, ReviewModelForm


class ProductFilterFormTestCase(TestCase):
    """Tests for the ProductFilterForm."""

    @classmethod
    def setUpTestData(cls) -> None:
        cls.form = ProductFilterForm()

    # * ------------ Testing the 'min_price' field's parameters --------------

    def test_min_price_field_required(self):
        """Test that the 'min_price' field is not required."""
        self.assertFalse(self.form.fields["min_price"].required)

    def test_min_price_field_label(self):
        """Test that the 'min_price' field's label is empty."""
        self.assertEqual(self.form.fields["min_price"].label, "")

    def test_min_price_field_min_value(self):
        """Test that the 'min_price' field's minimum value is 0."""
        self.assertEqual(self.form.fields["min_price"].min_value, 0)

    def test_min_price_field_decimal_places(self):
        """Test that the 'min_price' field's decimal places is 2."""
        self.assertEqual(self.form.fields["min_price"].decimal_places, 2)

    def test_min_price_field_widget(self):
        """Test that the 'min_price' field's widget is a NumberInput."""
        self.assertIsInstance(
            self.form.fields["min_price"].widget, forms.NumberInput
        )

    # * ------------ Testing the 'max_price' field's parameters --------------

    def test_max_price_field_required(self):
        """Test that the 'max_price' field is not required."""
        self.assertFalse(self.form.fields["max_price"].required)

    def test_max_price_field_label(self):
        """Test that the 'max_price' field's label is empty."""
        self.assertEqual(self.form.fields["max_price"].label, "")

    def test_max_price_field_min_value(self):
        """Test that the 'max_price' field's minimum value is 0."""
        self.assertEqual(self.form.fields["max_price"].min_value, 0)

    def test_max_price_field_decimal_places(self):
        """Test that the 'max_price' field's decimal places is 2."""
        self.assertEqual(self.form.fields["max_price"].decimal_places, 2)

    def test_max_price_field_widget(self):
        """Test that the 'max_price' field's widget is a NumberInput."""
        self.assertIsInstance(
            self.form.fields["max_price"].widget, forms.NumberInput
        )

    # * ------------- Testing the 'category' field's parameters --------------

    def test_category_field_required(self):
        """Test that the 'category' field is not required."""
        self.assertFalse(self.form.fields["category"].required)

    def test_category_field_label(self):
        """
        Test that the 'category' field's label is either None or 'Category'.
        """
        field = self.form.fields["category"]
        self.assertTrue(field.label is None or field.label == "Category")

    def test_category_field_widget(self):
        """Test that the 'category' field's widget is a RadioSelect."""
        self.assertIsInstance(
            self.form.fields["category"].widget, forms.RadioSelect
        )

    def test_category_field_queryset(self):
        """
        Test that the 'category' field's queryset is all objects in the Category model.
        """
        self.assertQuerysetEqual(
            self.form.fields["category"].queryset, Category.objects.all()
        )

    # * -------------- Testing the 'brands' field's parameters ---------------

    def test_brands_field_required(self):
        """Test that the 'brands' field is not required."""
        self.assertFalse(self.form.fields["brands"].required)

    def test_brands_field_label(self):
        """Test that the 'brands' field's label is 'Brand'."""
        self.assertEqual(self.form.fields["brands"].label, "Brand")

    def test_brands_field_widget(self):
        """
        Test that the 'brands' field's widget is a CheckboxSelectMultiple.
        """
        self.assertIsInstance(
            self.form.fields["brands"].widget, forms.CheckboxSelectMultiple
        )

    def test_brands_field_queryset(self):
        """
        Test that the 'brands' field's queryset is all objects in the Brand model.
        """
        self.assertQuerysetEqual(
            self.form.fields["brands"].queryset, Brand.objects.all()
        )

    # * -------------- Testing the 'years' field's parameters ----------------

    def test_years_field_required(self):
        """Test that the 'years' field is not required."""
        self.assertFalse(self.form.fields["years"].required)

    def test_years_field_label(self):
        """Test that the 'years' field's label is 'Year'."""
        self.assertEqual(self.form.fields["years"].label, "Year")

    def test_years_field_widget(self):
        """
        Test that the 'years' field's widget is a CheckboxSelectMultiple.
        """
        self.assertIsInstance(
            self.form.fields["years"].widget, forms.CheckboxSelectMultiple
        )


class ReviewModelFormTestCase(TestCase):
    """Tests for the ReviewModelForm."""

    @classmethod
    def setUpTestData(cls) -> None:
        cls.form = ReviewModelForm()

    # * --------------- Testing the 'name' field's parameters ----------------

    def test_name_field_not_required(self):
        """Test that the 'name' field is not required."""
        self.assertTrue(self.form.fields["name"].required)

    def test_name_field_label(self):
        """Test that the 'name' field's label is 'Username'."""
        self.assertEqual(self.form.fields["name"].label, "Username")

    def test_name_field_widget(self):
        """Test that the the 'name' field's widget is a TextInput."""
        self.assertIsInstance(self.form.fields["name"].widget, forms.TextInput)

    # * --------------- Testing the 'body' field's parameters ----------------

    def test_body_field_not_required(self):
        """Test that the 'body' field is not required."""
        self.assertTrue(self.form.fields["body"].required)

    def test_body_field_label(self):
        """Test that the 'body' field's label is 'Body'."""
        self.assertEqual(self.form.fields["body"].label, "Body")

    def test_body_field_widget(self):
        """Test that the 'body' field's widget is a Textarea."""
        self.assertIsInstance(self.form.fields["body"].widget, forms.Textarea)
