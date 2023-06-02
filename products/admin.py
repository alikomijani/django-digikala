from django.contrib import admin
from .models import Product, Category, Comment, Question, Answer,\
    Image, ProductOption, ProductPrice

# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'en_name', 'name', 'category']
    list_filter = ['category']
    search_fields = ['en_name', 'name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'parent']
    list_filter = ['parent']
    search_fields = ['name', 'description']
    fieldsets = (
        ('details', {
            'fields': ('name', 'slug', 'parent',
                       ('description',),)
        }),
        ('images', {
            'fields': ('icon', 'image',)
        }),

    )


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass
