from rest_framework.routers import DefaultRouter
from .views import SellerViewSet, SellerProductPriceViewSet

router = DefaultRouter()
router.register("sellers", SellerViewSet, basename="seller")
router.register(
    "seller-product-prices", SellerProductPriceViewSet, basename="sellerproductprice"
)

urlpatterns = router.urls
