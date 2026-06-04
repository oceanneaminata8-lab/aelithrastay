from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from aelithrastay.permissions import IsAdmin
from accounts.models import AdminLog
from .models import Booking
from .serializers import BookingSerializer


class AdminDisputeViewSet(viewsets.ReadOnlyModelViewSet):
    """Admin endpoint for managing booking disputes"""
    permission_classes = (IsAuthenticated, IsAdmin)
    serializer_class = BookingSerializer

    def get_queryset(self):
        # Only show bookings with disputes
        return Booking.objects.filter(dispute_status__in=[
            Booking.DisputeStatus.OPEN,
            Booking.DisputeStatus.REVIEWING,
        ]).select_related('guest', 'property', 'property__host')

    @action(detail=True, methods=['post'])
    def mark_reviewing(self, request, pk=None):
        """Mark dispute as under review"""
        booking = self.get_object()
        booking.dispute_status = Booking.DisputeStatus.REVIEWING
        booking.save()

        AdminLog.objects.create(
            admin=request.user,
            action_type=AdminLog.ActionType.DISPUTE_REVIEWING,
            object_type='booking',
            object_id=booking.id,
            details={'guest': booking.guest.username, 'property': booking.property.title}
        )

        serializer = self.get_serializer(booking)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        """Resolve a dispute"""
        booking = self.get_object()
        booking.dispute_status = Booking.DisputeStatus.RESOLVED
        booking.dispute_resolution = request.data.get('resolution', '')
        booking.save()

        AdminLog.objects.create(
            admin=request.user,
            action_type=AdminLog.ActionType.DISPUTE_RESOLVED,
            object_type='booking',
            object_id=booking.id,
            details={
                'guest': booking.guest.username,
                'property': booking.property.title,
                'resolution': booking.dispute_resolution
            }
        )

        serializer = self.get_serializer(booking)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get dispute statistics"""
        from django.db.models import Count
        stats = Booking.objects.filter(
            dispute_status__in=[
                Booking.DisputeStatus.OPEN,
                Booking.DisputeStatus.REVIEWING,
                Booking.DisputeStatus.RESOLVED,
            ]
        ).values('dispute_status').annotate(count=Count('id'))
        return Response(stats)
