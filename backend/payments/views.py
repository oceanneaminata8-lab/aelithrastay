from django.db.models import Q
from rest_framework import permissions, viewsets

from aelithrastay.permissions import IsBookingParticipant
from .models import Payment
from .serializers import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = (permissions.IsAuthenticated,)
    ordering_fields = ('created_at', 'status', 'amount')

    def get_queryset(self):
        user = self.request.user
        queryset = Payment.objects.select_related('booking', 'booking__guest', 'booking__property__host')
        if user.is_staff:
            return queryset
        return queryset.filter(Q(booking__guest=user) | Q(booking__property__host=user)).distinct()

    def check_object_permissions(self, request, obj):
        permission = IsBookingParticipant()
        if not permission.has_object_permission(request, self, obj.booking):
            self.permission_denied(request)
        super().check_object_permissions(request, obj)

    def perform_create(self, serializer):
        from django.db import IntegrityError
        from rest_framework.exceptions import ValidationError
        booking = serializer.validated_data['booking']
        if not (self.request.user.is_staff or booking.guest_id == self.request.user.id):
            self.permission_denied(self.request)
        try:
            serializer.save(amount=booking.total_price)
        except IntegrityError:
            raise ValidationError({"non_field_errors": ["A payment for this booking already exists."]})
