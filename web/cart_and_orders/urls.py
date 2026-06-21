from django.urls import path
from . import views

app_name = 'cart_and_orders'

urlpatterns = [
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-success/', views.order_success, name='order_success'),
    path('orders/', views.orders_view, name='orders'),  # Added this line
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
]
