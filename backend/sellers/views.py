from rest_framework import viewsets
from .models import Seller, SellerProductPrice
from .serializers import SellerSerializer, SellerProductPriceSerializer


class SellerViewSet(viewsets.ModelViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    lookup_field = "slug"  # allows /sellers/{slug}/ instead of ID


class SellerProductPriceViewSet(viewsets.ModelViewSet):
    queryset = SellerProductPrice.objects.select_related("product", "seller").all()
    serializer_class = SellerProductPriceSerializer
