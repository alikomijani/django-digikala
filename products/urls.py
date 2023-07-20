from .views import product_list_view, comment_api_response_rest,\
    ProductListView, ProductClassBaseView
from django.urls import path

app_name = 'products'
urlpatterns = [
    path('', product_list_view, name='product-list'),
    path('<int:pk>/comments/', comment_api_response_rest, name='comment_api'),
    path('<int:pk>/', ProductClassBaseView.as_view(), name='product_detail'),
    path('category/<slug:slug>/',
         ProductListView.as_view(), name='product_list'),
]
