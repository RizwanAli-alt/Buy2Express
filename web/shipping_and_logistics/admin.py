from django.contrib import admin
from .models import ShippingAddress, OrderTracking, ShippingProvider

@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'address_line_1', 'city', 'state', 'postal_code', 'country')  # Updated field names
    search_fields = ('user__username', 'city', 'state', 'country')  # Ensure user relationship and fields match

@admin.register(OrderTracking)
class OrderTrackingAdmin(admin.ModelAdmin):
    list_display = ('order', 'status', 'tracking_number', 'updated_at')  # Added 'tracking_number'
    list_filter = ('status',)
    search_fields = ('order__id', 'tracking_number')  # Allow searching by tracking number

@admin.register(ShippingProvider)
class ShippingProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_number', 'website')
    search_fields = ('name',)
