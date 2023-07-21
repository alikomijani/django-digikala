from .views import product_list_view, comment_api_response_rest,\
    ProductListView, ProductClassBaseView
from django.urls import path
from .api import ProductDetail, ProductList
app_name = 'products'
urlpatterns = [
    path('', product_list_view, name='product-list'),
    path('<int:pk>/comments/', comment_api_response_rest, name='comment_api'),
    path('<int:pk>/', ProductClassBaseView.as_view(), name='product_detail'),
    path('category/<slug:slug>/',
         ProductListView.as_view(), name='product_list'),
    path("api/products/", ProductList.as_view(), name="api-product-list"),
    path("api/products/<int:pk>", ProductDetail.as_view(),
         name="api-product-details")
]
