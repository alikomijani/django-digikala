from django.forms import formset_factory, inlineformset_factory, ModelForm
from django import forms
from products.models import Product, ProductOption, SellerProductPrice


class ProductModelForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class ProductOptionModelForm(ModelForm):
    class Meta:
        model = ProductOption
        fields = '__all__'


ProductOptionFormSet = inlineformset_factory(
    Product, ProductOption, fields=["name", "value"], )

SellerProductPriceFormSet = inlineformset_factory(
    Product, SellerProductPrice, fields=["seller", "price", "discount"], )
