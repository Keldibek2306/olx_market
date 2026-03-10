from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['reviewer', 'seller', 'rating', 'created_at']
    list_filter = ['rating']
    search_fields = ['reviewer__username', 'seller__username', 'comment']
    readonly_fields = ['created_at']
