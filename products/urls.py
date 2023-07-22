from .views import product_list_view, comment_api_response_rest,\
    ProductListView, ProductClassBaseView, basket_cart_view
from django.urls import path
from .api import ProductDetail, ProductList, ProductListGenericView,\
    ProductDetailGenericView, ProductModelViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'products', ProductModelViewSet)

app_name = 'products'
urlpatterns = [
    path('', product_list_view, name='product-list'),
    path('cart/', basket_cart_view, name='basket-cart'),
    path('<int:pk>/comments/', comment_api_response_rest, name='comment_api'),
    path('<int:pk>/', ProductClassBaseView.as_view(), name='product_detail'),
    path('category/<slug:slug>/',
         ProductListView.as_view(), name='product_list'),
] + router.urls
