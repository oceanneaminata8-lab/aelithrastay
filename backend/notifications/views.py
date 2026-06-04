from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from aelithrastay.permissions import IsOwner
from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    ordering_fields = ('created_at', 'is_read')

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.role == 'admin':
            return Notification.objects.select_related('user')
        return Notification.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        if self.request.user.is_staff or self.request.user.role == 'admin':
            serializer.save()
            return
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save(update_fields=['is_read'])
        return Response(self.get_serializer(notification).data, status=status.HTTP_200_OK)
