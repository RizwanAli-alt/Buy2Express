"""
Deals, Discounts, Coupons API.
"""
from django.utils import timezone
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from deals_and_discounts.models import Deal, Discount, Coupon
from ..serializers.deals import DealSerializer, DiscountSerializer, CouponSerializer
from ..utils import SmallPagination, IsAdminOrReadOnly


class DealViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class   = DealSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class   = SmallPagination

    def get_queryset(self):
        return Deal.objects.filter(is_active=True, end_date__gte=timezone.now()).order_by('start_date')


class DiscountViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class   = DiscountSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class   = SmallPagination

    def get_queryset(self):
        return Discount.objects.filter(is_active=True, end_date__gte=timezone.now()).order_by('start_date')


class ApplyCouponView(APIView):
    """
    POST /api/v1/coupons/apply/

    Body: { code: "SAVE20" }
    Returns coupon details if valid, or 404/400 if not.
    """
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request):
        code = request.data.get('code', '').strip().upper()
        if not code:
            return Response({'detail': 'Coupon code is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            coupon = Coupon.objects.get(code=code, active=True, valid_until__gte=timezone.now())
        except Coupon.DoesNotExist:
            return Response({'detail': 'Invalid or expired coupon.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(CouponSerializer(coupon).data)