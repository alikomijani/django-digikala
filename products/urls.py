from .views import index, product_view
from django.urls import path

urlpatterns = [
    path('', index),
    path('products/<int:product_id>', product_view),
]
