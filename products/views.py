from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from products.forms import ProductCommentModelForm
from .models import Product, Category, Comment
import json
from django.views import View
from django.views.generic import ListView, DetailView
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import CommentModelSerializer
# Create your views here.


def basket_cart_view(request):
    """Simple View to Order a Product for an User in Basket Cart"""

    user, product = request.user, Product.objects.first()
    print(user.balance)
    print(product.default_product_seller.price)
    return HttpResponse("Successfully")


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


class ProductDetailView(DetailView):
    model = Product
    queryset = Product.objects.exclude(is_active=False)


class ProductClassBaseView(View):
    form_class = ProductCommentModelForm
    template_name = "products/product_detail.html"

    def get(self, request, pk, *args, **kwargs):
        p = get_object_or_404(Product.objects.select_related(
            'category'), pk=pk)
        form = self.form_class(initial={'product': p})
        context = {
            "default_product_seller": p.sellers_last_price[0],
            "product": p,
            "product_sellers": p.sellers_last_price,
            "comment_counts": p.comment_set.all().count(),
            'comment_form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, pk, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.save()
        return redirect('products:product_detail', pk=pk)


def product_detail_view(request, pk):
    p = get_object_or_404(Product.objects.select_related(
        'category').prefetch_related("comment_set"), pk=pk)

    if request.method == "GET":
        form = ProductCommentModelForm(initial={'product': p})
    elif request.method == 'POST':
        form = ProductCommentModelForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.save()
            return redirect('products:product_detail', pk=pk)
    context = {
        "default_product_seller": p.sellers_last_price[0],
        "product": p,
        "product_sellers": p.sellers_last_price,
        "comments": p.comment_set.all(),
        "comment_counts": p.comment_set.all().count(),
        'comment_form': form
    }
    return render(
        template_name='products/product_detail.html',
        request=request,
        context=context
    )


def home(request):
    query = Product.objects.all()
    most_off_products = query
    most_sell = query
    most_recent = query
    context = {
        "most_off_products": most_off_products,
        "most_sell": most_sell,
        "most_recent": most_recent,
        "banners": [],
    }

    return render(
        template_name='products/index.html',
        request=request,
        context=context
    )


class ProductListView(ListView):
    model = Product
    context_object_name = "product_list"
    queryset = Product.objects.exclude(is_active=False)

    def get_queryset(self) -> QuerySet[Any]:
        query = super().get_queryset()
        category = Category.objects.get(slug=self.kwargs['slug'])
        self.category = category
        query = query.filter(
            category__slug__in=[self.kwargs['slug'], *category.children],
            name__contains=self.request.GET.get('search', ''))
        return query

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context["category"] = self.category
        return context


@csrf_exempt
def comment_api_response(request, pk):
    if request.method == 'GET':
        comments = Comment.objects.filter(product_id=pk).select_related('user')
        comment_list = []
        for comment in comments:
            comment_list.append(comment.to_dict())
        context = {
            "result": comment_list,
            "count": comments.count(),
        }
        return HttpResponse(content=json.dumps(context),
                            content_type='application/json')

    else:
        form = ProductCommentModelForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product_id = pk
            comment.save()
            context = comment.to_dict()
            return HttpResponse(content=json.dumps(context),
                                content_type='application/json')
        else:
            return HttpResponse(content=json.dumps({'message': "error"}),
                                content_type='application/json', status=400)


@api_view(["POST", "GET"])
def comment_api_response_rest(request, pk):
    if request.method == 'GET':
        comments = Comment.objects.filter(product_id=pk).select_related('user')
        serializer = CommentModelSerializer(instance=comments, many=True)
        return Response(data=serializer.data)
    else:
        serializer = CommentModelSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=201)
