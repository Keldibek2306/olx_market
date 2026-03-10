from django.contrib import admin
from .models import SellerProfile


@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ['shop_name', 'user', 'region', 'district', 'rating', 'total_sales', 'created_at']
    list_filter = ['region']
    search_fields = ['shop_name', 'user__username']
    readonly_fields = ['rating', 'total_sales', 'created_at', 'updated_at']
