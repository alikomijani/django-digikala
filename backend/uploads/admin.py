from django.contrib import admin
from .models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("alt", "content_object", "is_default", "created_at", "updated_at")
    list_filter = ("is_default", "content_type")
    search_fields = ("alt",)
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)

    def get_queryset(self, request):
        """Optimize queryset to prefetch related objects for content_type"""
        qs = super().get_queryset(request)
        return qs.select_related("content_type")
