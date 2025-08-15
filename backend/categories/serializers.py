# serializers.py
from rest_framework import serializers
from .models import Brand, Category, CategoryAttribute


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "name", "en_name", "slug", "description", "images"]


class RecursiveCategorySerializer(serializers.Serializer):
    """Serializer for recursive category children"""

    id = serializers.IntegerField()
    name = serializers.CharField()
    slug = serializers.SlugField()
    is_active = serializers.BooleanField()
    children = serializers.ListSerializer(child=serializers.DictField())


class CategoryAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryAttribute
        fields = [
            "id",
            "name",
            "slug",
            "data_type",
            "is_required",
            "options",
        ]


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    category_attributes = CategoryAttributeSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "parent",
            "is_active",
            "images",
            "children",
            "category_attributes",
        ]

    def get_children(self, obj):
        return CategorySerializer(obj.children.all(), many=True).data


class CategoryCreateUpdateSerializer(serializers.ModelSerializer):
    """Separate serializer for create/update without recursive children."""

    class Meta:
        model = Category
        fields = [
            "name",
            "slug",
            "description",
            "parent",
            "is_active",
            "images",
        ]
