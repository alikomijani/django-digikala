from .serializer import ProductSerializer, ProductListSerializer
from .models import Product
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from .permissions import IsAdminOrReadOnly
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend


class ProductList(APIView):
    permission_classes = (IsAdminOrReadOnly,)

    def get(self, request, format=None):
        query = Product.objects.all().select_related('brand', 'category')
        serializer = ProductListSerializer(instance=query, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProductListSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


class ProductDetail(APIView):
    permission_classes = (IsAdminOrReadOnly,)

    def get_object(self, pk):
        try:
            return Product.objects.select_related('brand', 'category').get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        object = self.get_object(pk)
        serializer = ProductSerializer(instance=object,)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        object = self.get_object(pk)
        serializer = ProductSerializer(instance=object, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        object = self.get_object(pk)
        object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductListGenericView(generics.ListCreateAPIView):
    serializer_class = ProductListSerializer
    queryset = Product.objects.all()


class ProductDetailGenericView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all().select_related(
        'brand', 'category').prefetch_related('sellers')


class ProductModelViewSet(ModelViewSet):
    serializer_class = ProductListSerializer
    queryset = Product.objects.all()
    filterset_fields = ['category', 'brand']
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'en_name']

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'create':
            return self.serializer_class
        else:
            return ProductSerializer

    @action(detail=True, methods=["post"], )
    def like(self, request, pk):
        product: Product = self.get_object()
        product.liked_users.add(request.user)
        serializer = self.get_serializer(instance=product)
        return Response(data=serializer.data,)
