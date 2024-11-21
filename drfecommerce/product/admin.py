from django.contrib import admin
from .models import Category, Brand, Product


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent']
    list_filter = ['name', 'parent']
    search_fields = ['name']


class BrandgAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'id']
    list_filter = ['name']
    search_fields = ['name']


class ProductgAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'is_digital', 'brand', 'category']
    list_filter = ['name', 'is_digital', 'brand', 'category']
    search_fields = ['name']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandgAdmin)
admin.site.register(Product, ProductgAdmin)

