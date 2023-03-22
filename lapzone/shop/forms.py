from django import forms
from django.db.models import QuerySet

from .models import Product, Brand


class ProductFilterForm(forms.Form):
    """Form for filtering products by brand, and year."""

    brand = forms.ModelMultipleChoiceField(
        queryset=Brand.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
    year = forms.MultipleChoiceField(
        choices=[
            (year, year)
            for year in set(
                map(
                    lambda tup: int(tup[0]),
                    Product.objects.all().values_list("year"),
                )
            )
        ],
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    def get_filtered_products(self) -> QuerySet[Product]:
        """Returns a QuerySet with filtered products or all."""

        products = Product.objects.all()
        if self.cleaned_data.get("brand"):
            products = products.filter(brand__in=self.cleaned_data["brand"])
        if self.cleaned_data.get("year"):
            products = products.filter(year__in=self.cleaned_data["year"])
        return products
