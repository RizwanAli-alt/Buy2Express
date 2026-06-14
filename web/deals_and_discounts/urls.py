from django.urls import path
from . import views

app_name = 'deals_and_discounts'

urlpatterns = [
    path('deals/', views.deal_list, name='deal_list'),
    path('deals/create/', views.deal_create, name='deal_create'),
    path('discounts/', views.discount_list, name='discount_list'),
    path('discounts/create/', views.discount_create, name='discount_create'),
    path('apply-coupon/', views.apply_coupon, name='apply_coupon'),
]
