from django import forms
from django.db.models import QuerySet

from . import services
from .models import Product, Review


class ProductFilterForm(forms.Form):
    """Form for filtering products."""

    min_price = forms.DecimalField(
        min_value=0,
        decimal_places=2,
        label="",
        required=False,
        widget=forms.NumberInput(
            attrs={"class": "form-control mb-2", "placeholder": "Min price"}
        ),
    )
    max_price = forms.DecimalField(
        min_value=0,
        decimal_places=2,
        label="",
        required=False,
        widget=forms.NumberInput(
            attrs={"class": "form-control mb-2", "placeholder": "Max price"}
        ),
    )
    category = forms.ModelChoiceField(
        queryset=services.get_all_categories(),
        widget=forms.RadioSelect,
        required=False,
    )
    brands = forms.ModelMultipleChoiceField(
        queryset=services.get_all_brands(),
        widget=forms.CheckboxSelectMultiple,
        label="Brand",
        required=False,
    )
    years = forms.MultipleChoiceField(
        choices=[
            (year, year)
            for year in set(
                map(
                    lambda tup: int(tup[0]),
                    Product.objects.all().values_list("year"),
                )
            )
        ],
        widget=forms.CheckboxSelectMultiple,
        label="Year",
        required=False,
    )

    def get_filtered_(self, products: QuerySet[Product]) -> QuerySet[Product]:
        """Returns the filtered given products."""
        if self.cleaned_data.get("min_price"):
            products = products.filter(
                price__gte=self.cleaned_data.get("min_price")
            )
        if self.cleaned_data.get("max_price"):
            products = products.filter(
                price__lte=self.cleaned_data.get("max_price")
            )
        if self.cleaned_data.get("category"):
            products = products.filter(category=self.cleaned_data["category"])
        if self.cleaned_data.get("brands"):
            products = products.filter(brand__in=self.cleaned_data["brands"])
        if self.cleaned_data.get("years"):
            products = products.filter(year__in=self.cleaned_data["years"])
        return products


dict_with_field_classes = {"class": "form-control w-50 mb-2"}


class ReviewModelForm(forms.ModelForm):
    """Model form for adding review to product."""

    class Meta:
        """Meta options for the ReviewForm."""

        model = Review
        fields = ("name", "body")
        widgets = {
            "name": forms.TextInput(attrs=dict_with_field_classes),
            "body": forms.Textarea(attrs=dict_with_field_classes),
        }
