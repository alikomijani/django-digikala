from django.shortcuts import render, HttpResponse
from .models import Category, Product

# Create your views here.


def index(request):
    categories = Category.objects.all()
    products = Product.objects.all()[:10]
    category_response = ''
    for c in categories:
        category_response += f'<li>{c.name}</li>'
    category_response = f"<ul>{category_response}</ul>"

    product_response = ''
    for p in products:
        product_response += f'<li><a href="/products/{p.id}">{p.name}</a></li>'
    product_response = f"<ul>{product_response}</ul>"

    return HttpResponse(f"""
                        <html>
                        <head><title>Digikala</title></head>
                        <body>
                        <h1>the best seller site in iran</h1>
                        {category_response}
                        {product_response}
                        </body>
                        </html>
                        """)


def product_view(request, product_id):
    try:
        p = Product.objects.get(id=product_id)
        return HttpResponse(f"""
                        <html>
                        <head><title>Digikala</title></head>
                        <body>
                        <h1> {p.name}</h1>
                        <h5>{p.en_name}</h5>
                        <p>{p.description}</p>
                        </body>
                        </html>
                        """)
    except Product.DoesNotExist:
        return HttpResponse('404 Products not found')
