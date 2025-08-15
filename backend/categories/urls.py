from rest_framework.routers import DefaultRouter
from .views import BrandViewSet, CategoryViewSet, CategoryAttributeViewSet

router = DefaultRouter()
router.register("brands", BrandViewSet, basename="brand")
router.register("categories", CategoryViewSet, basename="category")
router.register(
    "category-attributes", CategoryAttributeViewSet, basename="categoryattribute"
)

urlpatterns = router.urls
