from django.contrib import admin
from django.utils.html import format_html
from .models import SearchQuery, Recommendation


@admin.register(SearchQuery)
class SearchQueryAdmin(admin.ModelAdmin):
    list_display = ('user', 'query', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('query', 'user__username')
    autocomplete_fields = ('user',)
    list_select_related = ('user',)
    ordering = ('-timestamp',)
    date_hierarchy = 'timestamp'
    list_per_page = 40
    readonly_fields = ('timestamp',)


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'score_badge', 'created_at')
    list_filter = ('score', 'created_at')
    search_fields = ('user__username', 'product__name')
    autocomplete_fields = ('user', 'product')
    list_select_related = ('user', 'product')
    ordering = ('-score', '-created_at')
    date_hierarchy = 'created_at'
    list_per_page = 40
    actions = ('delete_low_score_recommendations',)

    @admin.display(description='Score')
    def score_badge(self, obj):
        try:
            score = float(obj.score)
        except (TypeError, ValueError):
            score = 0
        if score >= 0.75:
            color = '#2E7D32'
        elif score >= 0.4:
            color = '#F5A623'
        else:
            color = '#E24B4A'
        return format_html(
            '<span style="background:{}; color:#fff; padding:3px 10px; '
            'border-radius:12px; font-size:11px; font-weight:700;">{}</span>',
            color, obj.score,
        )

    @admin.action(description='Delete recommendations scoring below 0.4')
    def delete_low_score_recommendations(self, request, queryset):
        deleted_count = queryset.filter(score__lt=0.4).delete()[0]
        self.message_user(request, f'{deleted_count} low-score recommendation(s) deleted.')