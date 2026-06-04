from rest_framework import permissions, viewsets

from aelithrastay.permissions import IsOwner
from .models import Review
from .serializers import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwner)
    search_fields = ('comment', 'property__title')
    ordering_fields = ('rating', 'created_at')

    def get_queryset(self):
        queryset = Review.objects.select_related('guest', 'property', 'booking')
        user = self.request.user
        if not (user.is_authenticated and (user.is_staff or user.role == 'admin')):
            queryset = queryset.exclude(moderation_status=Review.ModerationStatus.HIDDEN)
        property_id = self.request.query_params.get('property')
        if property_id:
            queryset = queryset.filter(property_id=property_id)
        return queryset

    def perform_create(self, serializer):
        from django.db import IntegrityError
        from rest_framework.exceptions import ValidationError
        try:
            serializer.save()
        except IntegrityError:
            raise ValidationError({"non_field_errors": ["You have already reviewed this property."]})
