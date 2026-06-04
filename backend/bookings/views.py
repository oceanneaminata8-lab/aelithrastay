from django.db.models import Q
from rest_framework import permissions, viewsets

from aelithrastay.permissions import IsBookingParticipant
from .models import Booking
from .serializers import BookingSerializer


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = (permissions.IsAuthenticated, IsBookingParticipant)
    ordering_fields = ('check_in', 'check_out', 'created_at', 'status')

    def get_queryset(self):
        user = self.request.user
        queryset = Booking.objects.select_related('guest', 'property', 'property__host')
        if user.is_staff or user.role == 'admin':
            return queryset
        return queryset.filter(Q(guest=user) | Q(property__host=user)).distinct()

    def perform_create(self, serializer):
        serializer.save(guest=self.request.user)
