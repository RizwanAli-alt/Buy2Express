"""
Shared utilities: pagination, filtering, ordering, permissions.
"""
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, SAFE_METHODS


# ── Pagination ────────────────────────────────────────────────────────────────

class StandardPagination(PageNumberPagination):
    """
    Default pagination: 20 items/page, configurable via ?page_size=N (max 100).
    Response shape:
        {
          "count": 250,
          "total_pages": 13,
          "next": "https://…?page=3",
          "previous": "https://…?page=1",
          "results": [ … ]
        }
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'count':       self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'next':        self.get_next_link(),
            'previous':    self.get_previous_link(),
            'results':     data,
        })


class SmallPagination(PageNumberPagination):
    """Used for lists that rarely exceed 50 items (categories, brands, etc.)."""
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 200


# ── Permissions ───────────────────────────────────────────────────────────────

class IsOwnerOrReadOnly(BasePermission):
    """Object-level: allow write only to the owner; everyone can read."""
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        owner = getattr(obj, 'user', getattr(obj, 'owner', None))
        return owner == request.user


class IsAdminOrReadOnly(BasePermission):
    """Allow admins full access; everyone else read-only."""
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_staff