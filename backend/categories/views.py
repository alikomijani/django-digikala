from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Brand, Category, CategoryAttribute
from .serializers import (
    BrandSerializer,
    CategorySerializer,
    CategoryCreateUpdateSerializer,
    CategoryAttributeSerializer,
)


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    lookup_field = "slug"


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().prefetch_related(
        "children", "category_attributes"
    )
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return CategoryCreateUpdateSerializer
        return CategorySerializer

    @action(detail=False, methods=["get"])
    def root(self, request):
        """Return only root categories"""
        roots = Category.objects.root().prefetch_related("children")
        serializer = CategorySerializer(roots, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def children(self, request, slug=None):
        """Return direct children of a category"""
        category = self.get_object()
        serializer = CategorySerializer(category.children.all(), many=True)
        return Response(serializer.data)


class CategoryAttributeViewSet(viewsets.ModelViewSet):
    queryset = CategoryAttribute.objects.select_related("category")
    serializer_class = CategoryAttributeSerializer
