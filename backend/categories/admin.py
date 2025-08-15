# admin.py
from django.contrib import admin
from .models import Brand, Category, CategoryAttribute


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "en_name", "slug")
    search_fields = ("name", "en_name", "slug")
    prepopulated_fields = {"slug": ("name",)}


class CategoryAttributeInline(admin.TabularInline):
    model = CategoryAttribute
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "parent", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [CategoryAttributeInline]


@admin.register(CategoryAttribute)
class CategoryAttributeAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "category", "data_type", "is_required")
    list_filter = ("data_type", "is_required")
    search_fields = ("name", "slug", "category__name")
    prepopulated_fields = {"slug": ("name",)}
