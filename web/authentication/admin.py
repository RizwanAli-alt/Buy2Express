from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_active', 'date_joined', 'is_verified')
    list_filter = ('role', 'is_active', 'is_verified')
    search_fields = ('username', 'email', 'contact_number')
