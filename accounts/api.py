from .serializers import UserChangePasswordSerializer, UserInfoSerializer,\
    UserRegisterSerializer
from .models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


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
