from django.contrib import admin
from django.utils.html import format_html
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating_stars', 'approved_badge', 'created_at')
    list_filter = ('rating', 'is_approved', 'created_at')
    search_fields = ('user__username', 'product__name')
    autocomplete_fields = ('user', 'product')
    list_select_related = ('user', 'product')
    date_hierarchy = 'created_at'
    list_per_page = 30
    actions = ('approve_reviews', 'reject_reviews')

    @admin.display(description='Rating')
    def rating_stars(self, obj):
        full = max(0, min(5, int(obj.rating or 0)))
        return '★' * full + '☆' * (5 - full)

    @admin.display(description='Status')
    def approved_badge(self, obj):
        color = '#2E7D32' if obj.is_approved else '#F5A623'
        label = 'Approved' if obj.is_approved else 'Pending'
        return format_html(
            '<span style="background:{}; color:#fff; padding:3px 10px; '
            'border-radius:12px; font-size:11px; font-weight:700;">{}</span>',
            color, label,
        )

    @admin.action(description='Approve selected reviews')
    def approve_reviews(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} review(s) approved.')

    @admin.action(description='Reject selected reviews')
    def reject_reviews(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'{updated} review(s) rejected.')