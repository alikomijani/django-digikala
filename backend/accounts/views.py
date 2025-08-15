from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from reviews.serializers import CommentSerializer, QuestionSerializer
from .utils import generate_otp
from digikala.paginators import BasePageNumberPagination
from reviews.models import Comment, Question

from .serializers import (
    OTPRequestSerializer,
    UserChangePasswordSerializer,
    UserInfoSerializer,
    UserRegisterSerializer,
)
from products.serializers import ProductLikeSerializer
from .models import User

from .serializers import OTPLoginSerializer


class UserRegisterView(generics.CreateAPIView):
    """Endpoint for user registration."""

    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]


class UserProfileViewSet(viewsets.ViewSet):
    """
    User profile management:
    - Retrieve / update user info
    - Change password
    - Get liked products
    - Get user comments
    - Get user questions
    """

    permission_classes = [IsAuthenticated]

    def get_user(self):
        return self.request.user

    def retrieve(self, request, pk=None):
        """GET /user-profile/ -> user info"""
        serializer = UserInfoSerializer(self.get_user())
        return Response(serializer.data)

    def update(self, request, pk=None):
        """PUT /user-profile/ -> update user info"""
        serializer = UserInfoSerializer(
            instance=self.get_user(), data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def change_password(self, request):
        """POST /user-profile/change-password/"""
        serializer = UserChangePasswordSerializer(
            instance=self.get_user(), data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "Password updated successfully."}, status=status.HTTP_200_OK
        )

    def paginate_queryset(self, queryset, serializer_class):
        """Helper function for paginated responses"""
        paginator = BasePageNumberPagination()
        page = paginator.paginate_queryset(queryset, self.request)
        serializer = serializer_class(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @action(detail=False, methods=["get"])
    def liked_products(self, request):
        """GET /user-profile/liked-products/"""
        user = self.get_user()
        queryset = user.liked_products.all()  # Assuming a reverse relation exists
        return self.paginate_queryset(queryset, ProductLikeSerializer)

    @action(detail=False, methods=["get"])
    def comments(self, request):
        """GET /user-profile/comments/"""
        user = self.get_user()
        queryset = Comment.objects.filter(user=user).order_by("-created_at")
        return self.paginate_queryset(queryset, CommentSerializer)

    @action(detail=False, methods=["get"])
    def questions(self, request):
        """GET /user-profile/questions/"""
        user = self.get_user()
        queryset = Question.objects.filter(user=user).order_by("-created_at")
        return self.paginate_queryset(queryset, QuestionSerializer)


class OTPRequestView(generics.GenericAPIView):
    serializer_class = OTPRequestSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data["mobile"]
        user, created = User.objects.get_or_create(mobile=mobile)

        session_id = generate_otp(user)

        return Response(
            {"detail": "OTP sent successfully.", "session_id": session_id},
            status=status.HTTP_200_OK,
        )


# ------------------------
# OTP Verify / Login
# ------------------------


class OTPLoginView(generics.GenericAPIView):
    serializer_class = OTPLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save()

        return Response(
            {"detail": "Login successful.", "token": result["token"]},
            status=status.HTTP_200_OK,
        )
