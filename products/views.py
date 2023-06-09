from django.shortcuts import render, get_object_or_404
from .models import Product

# Create your views here.


def product_list_view(request):
    page = int(request.GET.get('page', 1))
    query = Product.objects.all()
    q = request.GET.get('q', '')
    if q:
        query = query.filter(name__contains=q)
    page_size = 10
    products = query[(page-1) * page_size:page*page_size]
    context = {"products": products}

    return render(
        template_name='products/product-list.html',
        request=request,
        context=context,
    )


def product_detail_view(request, pk):
    p = get_object_or_404(Product, pk=pk)
    print(p.default_image.image.url)
    context = {"product": p}
    return render(
        template_name='products/product_detail.html',
        request=request,
        context=context
    )
