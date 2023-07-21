from rest_framework import serializers
from .models import Comment, Product, Brand, Category, SellerProductPrice
from sellers.serializers import SellerSerializer


class CommentModelSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id',
                  'text',
                  'title',
                  'product',
                  'rate',
                  'user')
        read_only_fields = ('user', 'product')
        model = Comment

    def create(self, validated_data):
        return super().create(validated_data)


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Brand


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = "__all__"
        model = Category


class ProductPrice(serializers.ModelSerializer):
    seller_details = SellerSerializer(
        source='seller',  read_only=True)

    class Meta:
        fields = "__all__"
        model = SellerProductPrice


class ProductSerializer(serializers.ModelSerializer):
    brand_details = BrandSerializer(source='brand', read_only=True)
    category_details = CategorySerializer(source='category', read_only=True)
    product_price_details = ProductPrice(
        source='seller_prices', many=True, read_only=True)

    class Meta:
        fields = "__all__"
        model = Product
