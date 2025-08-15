from django.contrib import admin
from django.utils.html import format_html
from .models import Product, ProductLike, ProductOption
from uploads.models import Image
from django.contrib.contenttypes.admin import GenericTabularInline


# Inline for images
class ImageInline(GenericTabularInline):
    model = Image
    extra = 1
    fields = ("alt", "image", "is_default", "created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")


# Inline for product options
class ProductOptionInline(admin.TabularInline):
    model = ProductOption
    extra = 1
    fields = ("attribute", "value")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "en_name",
        "category",
        "brand",
        "is_active",
        "min_price_display",
        "max_price_display",
    )
    list_filter = ("is_active", "category", "brand")
    search_fields = ("name", "en_name")
    inlines = [ImageInline, ProductOptionInline]
    readonly_fields = ("min_price_display", "max_price_display")

    def min_price_display(self, obj):
        return obj.min_price or "-"

    min_price_display.short_description = "Min Price"

    def max_price_display(self, obj):
        return obj.max_price or "-"

    max_price_display.short_description = "Max Price"


@admin.register(ProductLike)
class ProductLikeAdmin(admin.ModelAdmin):
    list_display = ("user", "product")
    list_filter = ("product",)
    search_fields = ("user__username", "product__name")


@admin.register(ProductOption)
class ProductOptionAdmin(admin.ModelAdmin):
    list_display = ("product", "attribute", "value")
    list_filter = ("attribute",)
    search_fields = ("product__name", "value")
