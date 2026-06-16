"""Payments API."""
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from cart_and_orders.models import Order
from ..serializers.payments import PaymentSerializer


class PaymentView(APIView):
    """
    POST /api/v1/payments/{order_id}/

    Body: { payment_method: "Card"|"Wallet"|"COD", ... }
    Returns the created payment record.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        serializer = PaymentSerializer(data=request.data, context={'order': order})
        serializer.is_valid(raise_exception=True)
        payment = serializer.save(order=order)

        if payment.is_successful():
            order.status = 'Paid'
            order.save(update_fields=['status'])

        return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)