# admin.py
from django.contrib import admin
from .models import Seller, SellerProductPrice


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(SellerProductPrice)
class SellerProductPriceAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "seller",
        "price",
        "discount",
        "discounted_price",
        "stock_quantity",
        "is_available",
        "update_at",
    )
    list_filter = ("is_available", "seller")
    search_fields = ("product__name", "seller__name")
    autocomplete_fields = ("product", "seller")
    readonly_fields = ("discounted_price", "discount_amount", "create_at", "update_at")
