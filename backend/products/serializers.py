from rest_framework import serializers
from .models import Product, ProductLike, ProductOption
from sellers.serializers import SellerProductPriceSerializer


class ProductOptionSerializer(serializers.ModelSerializer):
    attribute_name = serializers.CharField(source="attribute.name", read_only=True)

    class Meta:
        model = ProductOption
        fields = ["id", "product", "attribute", "attribute_name", "value"]
        read_only_fields = ["id"]


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    brand_name = serializers.CharField(source="brand.name", read_only=True)
    default_image_url = serializers.SerializerMethodField()
    sellers_last_price = SellerProductPriceSerializer(many=True, read_only=True)
    product_options = ProductOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "en_name",
            "description",
            "category",
            "category_name",
            "brand",
            "brand_name",
            "is_active",
            "default_image_url",
            "sellers_last_price",
            "product_options",
        ]

    def get_default_image_url(self, obj):
        default_image = obj.default_image
        if default_image and hasattr(default_image, "image") and default_image.image:
            return default_image.image.url
        return None


class ProductLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductLike
        fields = ["id", "user", "product"]
        read_only_fields = ["id"]
