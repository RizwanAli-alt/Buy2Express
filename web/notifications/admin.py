from django.contrib import admin
from django.utils.html import format_html
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'short_message', 'read_badge', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__username', 'message')
    autocomplete_fields = ('user',)
    date_hierarchy = 'created_at'
    list_select_related = ('user',)
    list_per_page = 40
    actions = ('mark_as_read', 'mark_as_unread')

    @admin.display(description='Message')
    def short_message(self, obj):
        return (obj.message[:70] + '…') if len(obj.message) > 70 else obj.message

    @admin.display(description='Status')
    def read_badge(self, obj):
        color = '#2E7D32' if obj.is_read else '#F5A623'
        label = 'Read' if obj.is_read else 'Unread'
        return format_html(
            '<span style="background:{}; color:#fff; padding:3px 10px; '
            'border-radius:12px; font-size:11px; font-weight:700;">{}</span>',
            color, label,
        )

    @admin.action(description='Mark selected notifications as read')
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} notification(s) marked as read.')

    @admin.action(description='Mark selected notifications as unread')
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} notification(s) marked as unread.')