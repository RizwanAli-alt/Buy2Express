from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'created_at', 'is_approved') 
    list_filter = ('rating', 'is_approved')  
    search_fields = ('user__username', 'product__name')