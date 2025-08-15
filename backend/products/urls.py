from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, ProductLikeViewSet, ProductOptionViewSet

router = DefaultRouter()
router.register(r"products", ProductViewSet)
router.register(r"product-likes", ProductLikeViewSet)
router.register(r"product-options", ProductOptionViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
