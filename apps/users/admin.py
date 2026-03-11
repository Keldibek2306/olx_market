from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):

    list_display = ['username', 'telegram_id', 'first_name', 'last_name', 'role', 'is_active', 'date_joined']
    list_filter = ['role', 'is_active']
    search_fields = ['username', 'first_name', 'last_name', 'telegram_id']
    ordering = ['-date_joined']

    readonly_fields = ['date_joined', 'last_login']  

    fieldsets = (
        (None, {'fields': ('username', 'telegram_id', 'password')}),

        ('Shaxsiy ma\'lumotlar', {
            'fields': ('first_name', 'last_name', 'phone_number', 'avatar')
        }),

        ('Ruxsatlar', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser')
        }),

        ('Muhim sanalar', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'telegram_id', 'first_name', 'role'),
        }),
    )