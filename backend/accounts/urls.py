from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from .views import (
    UserRegisterView,
    UserProfileViewSet,
    OTPRequestView,
    OTPLoginView,
)

router = DefaultRouter()
router.register(r"user-profile", UserProfileViewSet, basename="user-profile")

urlpatterns = [
    # User registration
    path("register/", UserRegisterView.as_view(), name="user-register"),
    # OTP login system
    path("otp/request/", OTPRequestView.as_view(), name="otp-request"),
    path("otp/verify/", OTPLoginView.as_view(), name="otp-login"),
    # Include viewset routes
    path("", include(router.urls)),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
