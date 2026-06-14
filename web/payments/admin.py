from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'payment_method', 'payment_status', 'transaction_id', 'payment_date')
    list_filter = ('payment_method', 'payment_status', 'payment_date')  
    search_fields = ('order__id', 'transaction_id', 'order__user__username') 
    ordering = ('-payment_date',)  
    readonly_fields = ('payment_date',)  
