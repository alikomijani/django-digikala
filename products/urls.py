from .views import product_list_view, product_single_view
from django.urls import path

app_name = 'products'
urlpatterns = [
    path('', product_list_view, name='product-list'),
    path('<int:product_id>/', product_single_view, name='product-single'),
]
