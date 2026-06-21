from django.contrib import admin
from django.utils.html import format_html
from .models import ShippingAddress, OrderTracking, ShippingProvider


STATUS_COLORS = {
    'pending': '#F5A623',
    'processing': '#6C63FF',
    'shipped': '#2D9CDB',
    'in transit': '#2D9CDB',
    'out for delivery': '#2D9CDB',
    'delivered': '#2E7D32',
    'cancelled': '#E24B4A',
    'returned': '#7B7E92',
}


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'address_line_1', 'city', 'state', 'postal_code', 'country')
    list_filter = ('country', 'state')
    search_fields = ('user__username', 'city', 'state', 'country', 'postal_code')
    autocomplete_fields = ('user',)
    list_select_related = ('user',)
    list_per_page = 30


@admin.register(OrderTracking)
class OrderTrackingAdmin(admin.ModelAdmin):
    list_display = ('order', 'status_badge', 'tracking_number', 'updated_at')
    list_filter = ('status',)
    search_fields = ('order__id', 'tracking_number')
    autocomplete_fields = ('order',)
    list_select_related = ('order',)
    date_hierarchy = 'updated_at'
    list_per_page = 30
    actions = ('mark_shipped', 'mark_delivered')

    @admin.display(description='Status')
    def status_badge(self, obj):
        color = STATUS_COLORS.get(str(obj.status).lower(), '#7B7E92')
        return format_html(
            '<span style="background:{}; color:#fff; padding:3px 10px; '
            'border-radius:12px; font-size:11px; font-weight:700; '
            'text-transform:capitalize;">{}</span>',
            color, obj.status,
        )

    @admin.action(description='Mark selected as Shipped')
    def mark_shipped(self, request, queryset):
        updated = queryset.update(status='shipped')
        self.message_user(request, f'{updated} tracking record(s) marked as shipped.')

    @admin.action(description='Mark selected as Delivered')
    def mark_delivered(self, request, queryset):
        updated = queryset.update(status='delivered')
        self.message_user(request, f'{updated} tracking record(s) marked as delivered.')


@admin.register(ShippingProvider)
class ShippingProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_number', 'website_link')
    search_fields = ('name',)
    list_per_page = 30

    @admin.display(description='Website')
    def website_link(self, obj):
        if obj.website:
            return format_html('<a href="{0}" target="_blank" rel="noopener">{0}</a>', obj.website)
        return '—'