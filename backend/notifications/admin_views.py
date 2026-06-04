from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from aelithrastay.permissions import IsAdmin
from .models import Notification
from .serializers import NotificationSerializer


class AdminNotificationViewSet(viewsets.ViewSet):
    """Admin endpoint for sending notifications to users"""
    permission_classes = (IsAuthenticated, IsAdmin)

    @action(detail=False, methods=['post'])
    def broadcast(self, request):
        """Send a notification to all users"""
        title = request.data.get('title')
        message = request.data.get('message')
        
        if not title or not message:
            return Response(
                {'error': 'Title and message are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        from django.contrib.auth import get_user_model
        User = get_user_model()
        users = User.objects.all()
        
        notifications = [
            Notification(user=user, title=title, message=message)
            for user in users
        ]
        Notification.objects.bulk_create(notifications)
        
        return Response(
            {'message': f'Notification sent to {len(notifications)} users'},
            status=status.HTTP_201_CREATED
        )

    @action(detail=False, methods=['post'])
    def send_to_role(self, request):
        """Send a notification to users with a specific role"""
        title = request.data.get('title')
        message = request.data.get('message')
        role = request.data.get('role')  # guest, host, admin
        
        if not title or not message or not role:
            return Response(
                {'error': 'Title, message, and role are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        from django.contrib.auth import get_user_model
        User = get_user_model()
        users = User.objects.filter(role=role)
        
        notifications = [
            Notification(user=user, title=title, message=message)
            for user in users
        ]
        Notification.objects.bulk_create(notifications)
        
        return Response(
            {'message': f'Notification sent to {len(notifications)} {role}s'},
            status=status.HTTP_201_CREATED
        )

    @action(detail=False, methods=['post'])
    def send_to_user(self, request):
        """Send a notification to a specific user"""
        title = request.data.get('title')
        message = request.data.get('message')
        user_id = request.data.get('user_id')
        
        if not title or not message or not user_id:
            return Response(
                {'error': 'Title, message, and user_id are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        notification = Notification.objects.create(user=user, title=title, message=message)
        serializer = NotificationSerializer(notification)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def admin_notifications(self, request):
        """Get all notifications for admin panel"""
        notifications = Notification.objects.all().order_by('-created_at')[:100]
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)
