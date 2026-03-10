from django.contrib import admin
from .models import Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'order', 'is_main']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'seller', 'category', 'price', 'status', 'view_count', 'created_at']
    list_filter = ['status', 'condition', 'price_type', 'region']
    search_fields = ['title', 'description', 'seller__username']
    readonly_fields = ['view_count', 'favorite_count', 'created_at', 'updated_at']
    inlines = [ProductImageInline]
    list_editable = ['status']
    ordering = ['-created_at']
