from .views import create_product
from django.urls import path

app_name = 'dashboard'
urlpatterns = [
    path('products', create_product, name='create-product')
]
