from django.contrib import admin
from .models import Product, Category, Comment, Question, Answer,\
    Image, ProductOption, ProductPrice

# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'parent']
