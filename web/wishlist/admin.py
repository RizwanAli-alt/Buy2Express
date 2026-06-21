from django.contrib import admin
from .models import Wishlist


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'added_at')
    search_fields = ('user__username', 'product__name')
    autocomplete_fields = ('user', 'product')
    list_select_related = ('user', 'product')
    date_hierarchy = 'added_at'
    list_per_page = 40