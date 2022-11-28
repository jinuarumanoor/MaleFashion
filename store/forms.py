from django import forms
from .models import Variation
from .models import Product


class VariationForm(forms.ModelForm):
    class Meta:
        model = Variation
        fields = (
            'product', 'variation_category', 'variation_value', 'is_active')

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            'product_name', 'slug', 'description', 'price','offer_price','percentage', 'images', 'is_available', 'stock', 'category')            