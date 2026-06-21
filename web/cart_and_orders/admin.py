from django.contrib import admin
from django.utils.html import format_html
from .models import Cart, CartItem, Order, OrderItem


STATUS_COLORS = {
    'pending': '#F5A623',
    'processing': '#6C63FF',
    'shipped': '#2D9CDB',
    'delivered': '#2E7D32',
    'completed': '#2E7D32',
    'cancelled': '#E24B4A',
    'refunded': '#7B7E92',
}


def status_badge(value):
    color = STATUS_COLORS.get(str(value).lower(), '#7B7E92')
    return format_html(
        '<span style="background:{}; color:#fff; padding:3px 10px; '
        'border-radius:12px; font-size:11px; font-weight:700; '
        'text-transform:capitalize;">{}</span>',
        color, value,
    )


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    autocomplete_fields = ('product', 'variant')
    fields = ('product', 'variant', 'quantity', 'line_total')
    readonly_fields = ('line_total',)

    @admin.display(description='Line total')
    def line_total(self, obj):
        try:
            return f'${obj.quantity * obj.product.price:.2f}'
        except (TypeError, AttributeError):
            return '—'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'item_count', 'cart_total', 'created_at')
    search_fields = ('user__username', 'user__email')
    autocomplete_fields = ('user',)
    date_hierarchy = 'created_at'
    list_select_related = ('user',)
    list_per_page = 30
    inlines = [CartItemInline]

    # Uses the reverse FK accessor for CartItem -> Cart. If you set a
    # custom related_name (e.g. related_name='items') swap accordingly.
    @admin.display(description='Items')
    def item_count(self, obj):
        return obj.items.count() if hasattr(obj, 'items') else obj.cartitem_set.count()

    @admin.display(description='Cart total')
    def cart_total(self, obj):
        items = obj.items.all() if hasattr(obj, 'items') else obj.cartitem_set.all()
        total = sum((i.quantity * i.product.price for i in items), 0)
        return f'${total:.2f}'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    autocomplete_fields = ('product', 'variant')
    fields = ('product', 'variant', 'quantity', 'price', 'line_total')
    readonly_fields = ('line_total',)

    @admin.display(description='Line total')
    def line_total(self, obj):
        try:
            return f'${obj.quantity * obj.price:.2f}'
        except TypeError:
            return '—'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status_display', 'total_price', 'item_count', 'created_at')
    list_display_links = ('id', 'user')
    list_filter = ('status', 'created_at')
    search_fields = ('id', 'user__username', 'user__email')
    autocomplete_fields = ('user',)
    date_hierarchy = 'created_at'
    list_select_related = ('user',)
    list_per_page = 25
    save_on_top = True
    inlines = [OrderItemInline]
    actions = ('mark_processing', 'mark_shipped', 'mark_delivered', 'mark_cancelled')

    @admin.display(description='Status')
    def status_display(self, obj):
        return status_badge(obj.status)

    @admin.display(description='Items')
    def item_count(self, obj):
        return obj.items.count() if hasattr(obj, 'items') else obj.orderitem_set.count()

    @admin.action(description='Mark selected orders as Processing')
    def mark_processing(self, request, queryset):
        updated = queryset.update(status='processing')
        self.message_user(request, f'{updated} order(s) marked as processing.')

    @admin.action(description='Mark selected orders as Shipped')
    def mark_shipped(self, request, queryset):
        updated = queryset.update(status='shipped')
        self.message_user(request, f'{updated} order(s) marked as shipped.')

    @admin.action(description='Mark selected orders as Delivered')
    def mark_delivered(self, request, queryset):
        updated = queryset.update(status='delivered')
        self.message_user(request, f'{updated} order(s) marked as delivered.')

    @admin.action(description='Mark selected orders as Cancelled')
    def mark_cancelled(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} order(s) marked as cancelled.')


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'variant', 'quantity')
    search_fields = ('cart__user__username', 'product__name')
    autocomplete_fields = ('cart', 'product', 'variant')
    list_select_related = ('cart', 'product', 'variant')
    list_per_page = 30


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'variant', 'quantity', 'price')
    search_fields = ('order__id', 'product__name')
    autocomplete_fields = ('order', 'product', 'variant')
    list_select_related = ('order', 'product', 'variant')
    list_per_page = 30