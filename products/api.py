from .serializer import ProductSerializer
from .models import Product
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from .permissions import IsAdminOrReadOnly


class ProductList(APIView):
    permission_classes = (IsAdminOrReadOnly,)

    def get(self, request, format=None):
        query = Product.objects.all().select_related('brand', 'category')
        serializer = ProductSerializer(instance=query, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)
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
