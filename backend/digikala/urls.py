from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("api/users/", include("accounts.urls")),
        path("api/categories/", include("categories.urls")),
        path("api/products/", include("products.urls")),
        path("api/reviews/", include("reviews.urls")),
        path("api/sellers/", include("sellers.urls")),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)
