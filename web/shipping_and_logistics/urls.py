from django.urls import path
from . import views

app_name = 'shipping_and_logistics'

urlpatterns = [
    path('addresses/', views.shipping_address_list, name='shipping_address_list'),
    path('addresses/create/', views.shipping_address_create, name='shipping_address_create'),
    path('tracking/<int:order_id>/', views.order_tracking_view, name='order_tracking_view'),
    path('providers/', views.shipping_provider_list, name='shipping_provider_list'),
    path('providers/create/', views.add_shipping_provider, name='add_shipping_provider'),
]
