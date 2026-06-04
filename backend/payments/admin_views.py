from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from aelithrastay.permissions import IsAdmin
from accounts.models import AdminLog
from .models import Payment
from .serializers import PaymentSerializer


class AdminPaymentViewSet(viewsets.ReadOnlyModelViewSet):
    """Admin endpoint for payment management and refunds"""
    permission_classes = (IsAuthenticated, IsAdmin)
    serializer_class = PaymentSerializer

    def get_queryset(self):
        queryset = Payment.objects.select_related('booking', 'booking__guest', 'booking__property__host')
        
        # Filter by status if provided
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset.order_by('-created_at')

    @action(detail=True, methods=['post'])
    def refund(self, request, pk=None):
        """Process a payment refund"""
        payment = self.get_object()
        
        if payment.status != Payment.Status.PAID:
            return Response(
                {'error': 'Only paid payments can be refunded'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        payment.status = Payment.Status.REFUNDED
        payment.save()

        AdminLog.objects.create(
            admin=request.user,
            action_type=AdminLog.ActionType.PAYMENT_REFUNDED,
            object_type='payment',
            object_id=payment.id,
            details={
                'booking': payment.booking.id,
                'guest': payment.booking.guest.username,
                'amount': str(payment.amount),
                'reason': request.data.get('reason', '')
            }
        )

        # Send notification to guest
        from notifications.models import Notification
        Notification.objects.create(
            user=payment.booking.guest,
            title='Refund Processed',
            message=f'Your refund of ${payment.amount} has been processed. Reason: {request.data.get("reason", "N/A")}'
        )

        serializer = self.get_serializer(payment)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get payment statistics"""
        from django.db.models import Count, Sum
        stats = {
            'by_status': list(Payment.objects.values('status').annotate(count=Count('id'))),
            'by_method': list(Payment.objects.values('method').annotate(count=Count('id'))),
            'total_revenue': Payment.objects.filter(status=Payment.Status.PAID).aggregate(total=Sum('amount'))['total'] or 0,
            'total_refunded': Payment.objects.filter(status=Payment.Status.REFUNDED).aggregate(total=Sum('amount'))['total'] or 0,
        }
        return Response(stats)
