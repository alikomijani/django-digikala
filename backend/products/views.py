from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Product, ProductLike, ProductOption
from .serializers import (
    ProductSerializer,
    ProductLikeSerializer,
    ProductOptionSerializer,
)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.active().prefetch_related("product_options")
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProductLikeViewSet(viewsets.ModelViewSet):
    queryset = ProductLike.objects.all()
    serializer_class = ProductLikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["post"], url_path="toggle")
    def toggle_like(self, request):
        user = request.user
        product_id = request.data.get("product")
        if not product_id:
            return Response({"detail": "Product ID is required"}, status=400)

        like, created = ProductLike.objects.get_or_create(
            user=user, product_id=product_id
        )
        if not created:
            like.delete()
            return Response({"liked": False})
        return Response({"liked": True})


class ProductOptionViewSet(viewsets.ModelViewSet):
    queryset = ProductOption.objects.all()
    serializer_class = ProductOptionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
