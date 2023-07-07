from django.shortcuts import render
from .forms import ProductOptionFormSet, ProductModelForm, SellerProductPriceFormSet
# Create your views here.


def create_product(request):
    inlines = (ProductOptionFormSet(), SellerProductPriceFormSet())

    form = ProductModelForm()
    form.inlines = inlines
    return render(request, 'dashboard/create-product.html', {"form": form})
