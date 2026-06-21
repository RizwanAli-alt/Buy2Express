from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from .models import Deal, Discount, Coupon


def period_status(start, end, active_flag):
    """Computes a human Live / Upcoming / Expired / Inactive label."""
    now = timezone.now()
    if not active_flag:
        return ('Inactive', '#7B7E92')
    if start and now < start:
        return ('Upcoming', '#6C63FF')
    if end and now > end:
        return ('Expired', '#E24B4A')
    return ('Live', '#2E7D32')


def status_pill(label, color):
    return format_html(
        '<span style="background:{}; color:#fff; padding:3px 10px; '
        'border-radius:12px; font-size:11px; font-weight:700;">{}</span>',
        color, label,
    )


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'status_badge', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('is_active', 'start_date', 'end_date')
    search_fields = ('title',)
    date_hierarchy = 'start_date'
    list_per_page = 30
    actions = ('activate_deals', 'deactivate_deals')

    @admin.display(description='Status')
    def status_badge(self, obj):
        label, color = period_status(obj.start_date, obj.end_date, obj.is_active)
        return status_pill(label, color)

    @admin.action(description='Activate selected deals')
    def activate_deals(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} deal(s) activated.')

    @admin.action(description='Deactivate selected deals')
    def deactivate_deals(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} deal(s) deactivated.')


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('product', 'discount_percentage', 'start_date', 'end_date', 'status_badge')
    list_filter = ('is_active', 'start_date', 'end_date')
    search_fields = ('product__name',)
    autocomplete_fields = ('product',)
    date_hierarchy = 'start_date'
    list_per_page = 30
    actions = ('activate_discounts', 'deactivate_discounts')

    @admin.display(description='Status')
    def status_badge(self, obj):
        label, color = period_status(obj.start_date, obj.end_date, obj.is_active)
        return status_pill(label, color)

    @admin.action(description='Activate selected discounts')
    def activate_discounts(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} discount(s) activated.')

    @admin.action(description='Deactivate selected discounts')
    def deactivate_discounts(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} discount(s) deactivated.')


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code_display', 'discount_percentage', 'valid_from', 'valid_until', 'status_badge')
    list_filter = ('active', 'valid_from', 'valid_until')
    search_fields = ('code',)
    date_hierarchy = 'valid_from'
    list_per_page = 30
    actions = ('activate_coupons', 'deactivate_coupons')

    @admin.display(description='Code')
    def code_display(self, obj):
        return format_html('<code style="font-weight:700;">{}</code>', obj.code.upper())

    @admin.display(description='Status')
    def status_badge(self, obj):
        label, color = period_status(obj.valid_from, obj.valid_until, obj.active)
        return status_pill(label, color)

    @admin.action(description='Activate selected coupons')
    def activate_coupons(self, request, queryset):
        updated = queryset.update(active=True)
        self.message_user(request, f'{updated} coupon(s) activated.')

    @admin.action(description='Deactivate selected coupons')
    def deactivate_coupons(self, request, queryset):
        updated = queryset.update(active=False)
        self.message_user(request, f'{updated} coupon(s) deactivated.')