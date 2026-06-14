from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('process/<int:order_id>/', views.payment_process, name='payment_process'),
    path('success/', views.payment_success, name='payment_success'),
]
