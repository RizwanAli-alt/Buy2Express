from django.contrib import admin
from django.utils.html import format_html
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'email', 'contact_number', 'role_badge',
        'is_active', 'is_verified', 'date_joined',
    )
    list_display_links = ('username', 'email')
    list_editable = ('is_active', 'is_verified')
    list_filter = ('role', 'is_active', 'is_verified', 'date_joined')
    search_fields = ('username', 'email', 'contact_number')
    ordering = ('-date_joined',)
    date_hierarchy = 'date_joined'
    list_per_page = 30
    actions = ('verify_users', 'unverify_users', 'activate_users', 'deactivate_users')

    # Tweak these keys/colors to match your actual `role` choices.
    ROLE_COLORS = {
        'admin': '#1A1D2E',
        'seller': '#6C63FF',
        'customer': '#F5A623',
    }

    @admin.display(description='Role')
    def role_badge(self, obj):
        color = self.ROLE_COLORS.get(str(obj.role).lower(), '#7B7E92')
        label = obj.get_role_display() if hasattr(obj, 'get_role_display') else obj.role
        return format_html(
            '<span style="background:{}; color:#fff; padding:3px 10px; '
            'border-radius:12px; font-size:11px; font-weight:700; '
            'text-transform:capitalize;">{}</span>',
            color, label,
        )

    @admin.action(description='Mark selected users as verified')
    def verify_users(self, request, queryset):
        updated = queryset.update(is_verified=True)
        self.message_user(request, f'{updated} user(s) marked as verified.')

    @admin.action(description='Mark selected users as unverified')
    def unverify_users(self, request, queryset):
        updated = queryset.update(is_verified=False)
        self.message_user(request, f'{updated} user(s) marked as unverified.')

    @admin.action(description='Activate selected users')
    def activate_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} user(s) activated.')

    @admin.action(description='Deactivate selected users')
    def deactivate_users(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} user(s) deactivated.')