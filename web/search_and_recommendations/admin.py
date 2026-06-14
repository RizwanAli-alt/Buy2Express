from django.contrib import admin
from .models import SearchQuery, Recommendation

@admin.register(SearchQuery)
class SearchQueryAdmin(admin.ModelAdmin):
    list_display = ('user', 'query', 'timestamp')
    list_filter = ('timestamp',)  # Filter by date for better admin usability
    search_fields = ('query', 'user__username')  # Added user search capability
    ordering = ('-timestamp',)  # Order by most recent searches

@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'score', 'created_at')
    list_filter = ('score', 'created_at')  # Allow filtering by score and date
    search_fields = ('user__username', 'product__name')  # Allow searching by username and product name
    ordering = ('-score', '-created_at')  # Order by highest score and latest recommendations
