from django.contrib import admin
from django.utils.html import format_html
from .models import Payment


STATUS_COLORS = {
    'completed': '#2E7D32',
    'success': '#2E7D32',
    'pending': '#F5A623',
    'failed': '#E24B4A',
    'cancelled': '#E24B4A',
    'refunded': '#7B7E92',
}


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'order_link', 'payment_method', 'status_badge',
        'transaction_id', 'order_total', 'payment_date',
    )
    list_display_links = ('id', 'order_link')
    list_filter = ('payment_method', 'payment_status', 'payment_date')
    search_fields = ('order__id', 'transaction_id', 'order__user__username')
    autocomplete_fields = ('order',)
    ordering = ('-payment_date',)
    date_hierarchy = 'payment_date'
    list_select_related = ('order', 'order__user')
    list_per_page = 30
    readonly_fields = ('payment_date',)
    actions = ('mark_completed', 'mark_failed', 'mark_refunded')

    @admin.display(description='Order')
    def order_link(self, obj):
        return f'Order #{obj.order_id} ({obj.order.user.username})'

    @admin.display(description='Order total')
    def order_total(self, obj):
        total = getattr(obj.order, 'total_price', None)
        return f'${total:.2f}' if total is not None else '—'

    @admin.display(description='Status')
    def status_badge(self, obj):
        color = STATUS_COLORS.get(str(obj.payment_status).lower(), '#7B7E92')
        return format_html(
            '<span style="background:{}; color:#fff; padding:3px 10px; '
            'border-radius:12px; font-size:11px; font-weight:700; '
            'text-transform:capitalize;">{}</span>',
            color, obj.payment_status,
        )

    @admin.action(description='Mark selected payments as Completed')
    def mark_completed(self, request, queryset):
        updated = queryset.update(payment_status='completed')
        self.message_user(request, f'{updated} payment(s) marked as completed.')

    @admin.action(description='Mark selected payments as Failed')
    def mark_failed(self, request, queryset):
        updated = queryset.update(payment_status='failed')
        self.message_user(request, f'{updated} payment(s) marked as failed.')

    @admin.action(description='Mark selected payments as Refunded')
    def mark_refunded(self, request, queryset):
        updated = queryset.update(payment_status='refunded')
        self.message_user(request, f'{updated} payment(s) marked as refunded.')