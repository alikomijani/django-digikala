from .views import product_list_view, brand_view, \
    ProductListView, ProductClassBaseView
from django.urls import path

app_name = 'products'
urlpatterns = [
    path('', product_list_view, name='product-list'),
    path('<int:pk>/', ProductClassBaseView.as_view(), name='product_detail'),
    path('brand/<slug:brand_slug>/', brand_view, name='brand_detail'),
    path('category/<slug:category_slug>/',
         ProductListView.as_view(), name='category_detail'),
]
