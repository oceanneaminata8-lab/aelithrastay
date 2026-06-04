from rest_framework import permissions, viewsets

from aelithrastay.permissions import IsOwner
from .models import Wishlist
from .serializers import WishlistSerializer


class WishlistViewSet(viewsets.ModelViewSet):
    serializer_class = WishlistSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user).select_related('property', 'property__host')

    def perform_create(self, serializer):
        from django.db import IntegrityError
        from rest_framework.exceptions import ValidationError
        try:
            serializer.save(user=self.request.user)
        except IntegrityError:
            raise ValidationError({"non_field_errors": ["This property is already in your wishlist."]})
