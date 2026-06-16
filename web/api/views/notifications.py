"""Notifications API."""
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from notifications.models import Notification
from ..serializers.notifications import NotificationSerializer
from ..utils import StandardPagination


class NotificationViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class   = NotificationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class   = StandardPagination

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')

    @action(detail=True, methods=['post'], url_path='read')
    def mark_read(self, request, pk=None):
        """POST /api/v1/notifications/{id}/read/"""
        notif = self.get_object()
        notif.is_read = True
        notif.save()
        return Response(self.get_serializer(notif).data)

    @action(detail=False, methods=['post'], url_path='read-all')
    def mark_all_read(self, request):
        """POST /api/v1/notifications/read-all/"""
        self.get_queryset().update(is_read=True)
        return Response({'detail': 'All notifications marked as read.'})