from .serializers import UserChangePasswordSerializer, UserInfoSerializer,\
    UserRegisterSerializer
from .models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.decorators import action
from products.serializer import ProductListSerializer


@api_view(["POST"])
def user_register(request):
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data)


@api_view(["POST", "GET"])
@permission_classes(IsAuthenticated,)
def user_info(request):
    user = request.user
    if request.method == 'GET':
        serializer = UserInfoSerializer(instance=user, )
        return Response(serializer.data)
    else:
        serializer = UserInfoSerializer(instance=user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


@api_view(["POST", ])
@permission_classes(IsAuthenticated,)
def user_change_password(request):
    user = request.user
    serializer = UserChangePasswordSerializer(instance=user, data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data)


class UserProfile(generics.RetrieveAPIView,
                  generics.CreateAPIView,
                  generics.UpdateAPIView):

    serializer_class = UserInfoSerializer

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegisterSerializer
        elif self.action == 'change_password':
            return UserChangePasswordSerializer
        elif self.action == 'liked_product':
            return ProductListSerializer
        else:
            return self.serializer_class

    @action(detail=True, methods=["post"])
    def change_password(self, request, pk=None):
        user = self.get_object()
        serializer = self.get_serializer(instance=user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def liked_product(self, request, pk):
        user = self.get_object()
        query = user.liked_products.all()
        serializer = self.get_serializer(data=query, many=True)
        return Response(serializer.data)
