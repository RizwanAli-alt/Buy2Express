"""Cart & Checkout serializers."""
from rest_framework import serializers
from cart_and_orders.models import Cart, CartItem, Order
from product_management.models import Product


class CartItemSerializer(serializers.ModelSerializer):
    product_id   = serializers.PrimaryKeyRelatedField(queryset=Product.objects.filter(is_active=True), source='product')
    product_name = serializers.CharField(source='product.name', read_only=True)
    unit_price   = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    subtotal     = serializers.SerializerMethodField()

    class Meta:
        model  = CartItem
        fields = ['id', 'product_id', 'product_name', 'variant', 'quantity', 'unit_price', 'subtotal']

    def get_subtotal(self, obj):
        return obj.product.price * obj.quantity


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(source='cartitem_set', many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model  = Cart
        fields = ['id', 'items', 'total']

    def get_total(self, obj):
        return sum(item.product.price * item.quantity for item in obj.cartitem_set.select_related('product'))


class CheckoutSerializer(serializers.Serializer):
    shipping_address_id = serializers.IntegerField()
    notes               = serializers.CharField(required=False, allow_blank=True)

    def validate_shipping_address_id(self, value):
        from shipping_and_logistics.models import ShippingAddress
        user = self.context['request'].user
        if not ShippingAddress.objects.filter(id=value, user=user).exists():
            raise serializers.ValidationError('Shipping address not found.')
        return value

    def create(self, validated_data):
        request    = self.context['request']
        cart_items = self.context['cart_items']
        cart       = Cart.objects.get(user=request.user)

        order = Order.objects.create(
            user        = request.user,
            total_price = sum(i.product.price * i.quantity for i in cart_items),
            notes       = validated_data.get('notes', ''),
        )
        for item in cart_items:
            order.items.create(
                product  = item.product,
                variant  = item.variant,
                quantity = item.quantity,
                price    = item.product.price,
            )
        cart.clear()
        return order