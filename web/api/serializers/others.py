"""
Serializers for: Orders, Reviews, Wishlist, Deals, Notifications, Shipping, Payments, Search.
Split into one file for brevity; in a real project you'd split per-domain.
"""
from rest_framework import serializers

# ── Orders ────────────────────────────────────────────────────────────────────
from cart_and_orders.models import Order


class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Order
        fields = ['id', 'total_price', 'status', 'created_at']


class OrderDetailSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model  = Order
        fields = ['id', 'total_price', 'status', 'notes', 'created_at', 'items']

    def get_items(self, obj):
        return [
            {
                'product_id':   item.product_id,
                'product_name': item.product.name,
                'variant':      str(item.variant) if item.variant else None,
                'quantity':     item.quantity,
                'price':        str(item.price),
            }
            for item in obj.items.select_related('product')
        ]


# ── Reviews ───────────────────────────────────────────────────────────────────
from reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    user     = serializers.StringRelatedField(read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model  = Review
        fields = ['id', 'product', 'user', 'username', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'user', 'username', 'created_at']


# ── Wishlist ──────────────────────────────────────────────────────────────────
from wishlist.models import Wishlist, FavoriteStore


class WishlistSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model  = Wishlist
        fields = ['id', 'product', 'product_name', 'added_at']
        read_only_fields = ['id', 'added_at']


class FavoriteStoreSerializer(serializers.ModelSerializer):
    seller_name = serializers.CharField(source='seller.name', read_only=True)

    class Meta:
        model  = FavoriteStore
        fields = ['id', 'seller', 'seller_name']
        read_only_fields = ['id']


# ── Deals & Discounts ─────────────────────────────────────────────────────────
from deals_and_discounts.models import Deal, Discount, Coupon


class DealSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Deal
        fields = ['id', 'title', 'description', 'discount_percent', 'start_date', 'end_date', 'is_active']


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Discount
        fields = ['id', 'name', 'amount', 'start_date', 'end_date', 'is_active']


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Coupon
        fields = ['id', 'code', 'discount_percent', 'valid_until']


# ── Notifications ─────────────────────────────────────────────────────────────
from notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Notification
        fields = ['id', 'message', 'is_read', 'created_at']
        read_only_fields = ['id', 'message', 'created_at']


# ── Shipping ──────────────────────────────────────────────────────────────────
from shipping_and_logistics.models import ShippingAddress, ShippingProvider, OrderTracking


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ShippingAddress
        fields = ['id', 'full_name', 'address_line1', 'address_line2', 'city', 'state', 'postal_code', 'country', 'phone']
        read_only_fields = ['id']


class ShippingProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ShippingProvider
        fields = ['id', 'name', 'tracking_url_template']


class OrderTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model  = OrderTracking
        fields = ['id', 'order', 'status', 'tracking_number', 'estimated_delivery', 'last_updated']


# ── Payments ──────────────────────────────────────────────────────────────────
from payments.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Payment
        fields = ['id', 'order', 'payment_method', 'payment_status', 'amount', 'created_at']
        read_only_fields = ['id', 'order', 'payment_status', 'created_at']

    def create(self, validated_data):
        order  = self.context['order']
        method = validated_data.get('payment_method')
        payment = Payment.objects.create(
            order          = order,
            payment_method = method,
            payment_status = 'Completed' if method in ['Card', 'Wallet', 'COD'] else 'Pending',
            **{k: v for k, v in validated_data.items() if k != 'payment_method'},
        )
        return payment


# ── Search / Recommendations ──────────────────────────────────────────────────
from search_and_recommendations.models import Recommendation
from product_management.models import Product


class RecommendationSerializer(serializers.ModelSerializer):
    product_name  = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model  = Recommendation
        fields = ['id', 'product', 'product_name', 'product_price', 'score']