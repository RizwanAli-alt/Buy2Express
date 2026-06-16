"""
Cart & Checkout API views.

GET    /api/v1/cart/              – view cart with items & totals
POST   /api/v1/cart/items/        – add item  { product_id, variant_id?, quantity }
PATCH  /api/v1/cart/items/{id}/   – update quantity
DELETE /api/v1/cart/items/{id}/   – remove item
POST   /api/v1/cart/checkout/     – place order from current cart
"""
from rest_framework import generics, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cart_and_orders.models import Cart, CartItem
from ..serializers.cart import CartSerializer, CartItemSerializer, CheckoutSerializer
from ..utils import IsOwnerOrReadOnly


class CartView(generics.RetrieveAPIView):
    """GET /api/v1/cart/ – return the authenticated user's cart."""
    serializer_class   = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return cart


class CartItemViewSet(viewsets.ModelViewSet):
    """
    POST   /api/v1/cart/items/       – add item to cart
    PATCH  /api/v1/cart/items/{id}/  – update quantity
    DELETE /api/v1/cart/items/{id}/  – remove item
    """
    serializer_class   = CartItemSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    http_method_names  = ['post', 'patch', 'delete', 'head', 'options']

    def get_queryset(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return CartItem.objects.filter(cart=cart).select_related('product')

    def perform_create(self, serializer):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        product_id = serializer.validated_data['product'].id
        # Increment quantity if item already in cart
        existing = CartItem.objects.filter(cart=cart, product_id=product_id).first()
        if existing:
            existing.quantity += serializer.validated_data.get('quantity', 1)
            existing.save()
        else:
            serializer.save(cart=cart)


class CheckoutView(APIView):
    """
    POST /api/v1/cart/checkout/

    Body: { shipping_address_id, notes? }
    Creates an Order from the current cart, clears the cart, returns the order.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = Cart.objects.filter(user=request.user).first()
        if not cart:
            return Response({'detail': 'Cart not found.'}, status=status.HTTP_400_BAD_REQUEST)

        cart_items = cart.cartitem_set.select_related('product')
        if not cart_items.exists():
            return Response({'detail': 'Cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CheckoutSerializer(data=request.data, context={'request': request, 'cart_items': cart_items})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        from ..serializers.orders import OrderDetailSerializer
        return Response(OrderDetailSerializer(order, context={'request': request}).data, status=status.HTTP_201_CREATED)