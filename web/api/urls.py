"""
Buy2Express REST API – v1 URL configuration
Mount this under /api/v1/ in your root urls.py:
    path('api/v1/', include('api.urls')),
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .views import (
    auth as auth_views,
    products as product_views,
    cart as cart_views,
    orders as order_views,
    reviews as review_views,
    wishlist as wishlist_views,
    deals as deal_views,
    notifications as notif_views,
    search as search_views,
    shipping as shipping_views,
    payments as payment_views,
)

router = DefaultRouter()

# ── Products ──────────────────────────────────────────────────────────────────
router.register(r'products',   product_views.ProductViewSet,  basename='product')
router.register(r'categories', product_views.CategoryViewSet, basename='category')
router.register(r'brands',     product_views.BrandViewSet,    basename='brand')

# ── Cart ──────────────────────────────────────────────────────────────────────
router.register(r'cart/items', cart_views.CartItemViewSet, basename='cartitem')

# ── Orders ────────────────────────────────────────────────────────────────────
router.register(r'orders', order_views.OrderViewSet, basename='order')

# ── Reviews ───────────────────────────────────────────────────────────────────
router.register(r'reviews', review_views.ReviewViewSet, basename='review')

# ── Wishlist ──────────────────────────────────────────────────────────────────
router.register(r'wishlist',        wishlist_views.WishlistViewSet,      basename='wishlist')
router.register(r'favorite-stores', wishlist_views.FavoriteStoreViewSet, basename='favoritestore')

# ── Deals & Discounts ─────────────────────────────────────────────────────────
router.register(r'deals',     deal_views.DealViewSet,     basename='deal')
router.register(r'discounts', deal_views.DiscountViewSet, basename='discount')

# ── Notifications ─────────────────────────────────────────────────────────────
router.register(r'notifications', notif_views.NotificationViewSet, basename='notification')

# ── Shipping ──────────────────────────────────────────────────────────────────
router.register(r'shipping/addresses', shipping_views.ShippingAddressViewSet, basename='shippingaddress')
router.register(r'shipping/providers', shipping_views.ShippingProviderViewSet, basename='shippingprovider')
router.register(r'shipping/tracking',  shipping_views.OrderTrackingViewSet,    basename='ordertracking')

urlpatterns = [
    # ── JWT Auth ──────────────────────────────────────────────────────────────
    path('auth/register/',      auth_views.RegisterView.as_view(),        name='auth-register'),
    path('auth/login/',         TokenObtainPairView.as_view(),             name='auth-login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(),                name='auth-token-refresh'),
    path('auth/token/verify/',  TokenVerifyView.as_view(),                 name='auth-token-verify'),
    path('auth/logout/',        auth_views.LogoutView.as_view(),           name='auth-logout'),
    path('auth/profile/',       auth_views.ProfileView.as_view(),          name='auth-profile'),

    # ── Cart (non-router actions) ─────────────────────────────────────────────
    path('cart/',         cart_views.CartView.as_view(),     name='cart'),
    path('cart/checkout/', cart_views.CheckoutView.as_view(), name='cart-checkout'),

    # ── Payments ──────────────────────────────────────────────────────────────
    path('payments/<int:order_id>/', payment_views.PaymentView.as_view(), name='payment-process'),

    # ── Search & Recommendations ──────────────────────────────────────────────
    path('search/',          search_views.SearchView.as_view(),          name='search'),
    path('recommendations/', search_views.RecommendationsView.as_view(), name='recommendations'),

    # ── Deals: apply coupon ───────────────────────────────────────────────────
    path('coupons/apply/', deal_views.ApplyCouponView.as_view(), name='apply-coupon'),

    # ── ViewSet router ────────────────────────────────────────────────────────
    path('', include(router.urls)),
]