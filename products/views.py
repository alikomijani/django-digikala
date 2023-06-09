from django.shortcuts import render, get_object_or_404
from .models import Product, SellerProductPrice, Comment
from django.db.models import Min, Max
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
    # s = p.seller_prices.all().values('id').annotate(
    #     min=Min('update_at'))
    # print(s)
    # print(d)
    if request.method == "POST":
        comment = Comment.objects.create(
            user_email=request.POST.get("user_email", ''),
            title=request.POST.get("title", ''),
            text=request.POST.get("text", ''),
            rate=int(request.POST.get("rate", 0)),
            product=p
        )
    seller_prices = SellerProductPrice.objects.raw(
        f"""select * from products_sellerproductprice 
        where product_id = {p.id}
        group by seller_id
        having Max(update_at)""")
    context = {"product": p, "seller_prices": seller_prices,
               "comment_counts": p.comment_set.all().count()}
    return render(
        template_name='products/product_detail.html',
        request=request,
        context=context
    )
