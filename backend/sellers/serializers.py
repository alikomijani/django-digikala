# serializers.py
from rest_framework import serializers
from .models import Seller, SellerProductPrice


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ["id", "name", "slug"]


class SellerProductPriceSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    seller_name = serializers.CharField(source="seller.name", read_only=True)
    discounted_price = serializers.ReadOnlyField()
    discount_amount = serializers.ReadOnlyField()

    class Meta:
        model = SellerProductPrice
        fields = [
            "id",
            "product",
            "product_name",
            "seller",
            "seller_name",
            "price",
            "discount",
            "stock_quantity",
            "is_available",
            "discounted_price",
            "discount_amount",
            "create_at",
            "update_at",
        ]
        read_only_fields = ["create_at", "update_at"]
