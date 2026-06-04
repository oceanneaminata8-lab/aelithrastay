from django.contrib.auth import get_user_model
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from aelithrastay.permissions import IsAdmin
from .models import AdminLog
from .serializers import AdminUserSerializer, AdminLogSerializer, UserSuspensionSerializer, UserRoleChangeSerializer

User = get_user_model()


class AdminUserViewSet(viewsets.ModelViewSet):
    """Admin endpoint for user management (suspend, activate, change role)"""
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = (IsAuthenticated, IsAdmin)

    @action(detail=True, methods=['post'])
    def suspend(self, request, pk=None):
        """Suspend a user account"""
        user = self.get_object()
        user.is_suspended = True
        user.save()

        # Log the action
        AdminLog.objects.create(
            admin=request.user,
            action_type=AdminLog.ActionType.USER_SUSPENDED,
            object_type='user',
            object_id=user.id,
            details={'username': user.username, 'email': user.email}
        )

        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Activate a suspended user account"""
        user = self.get_object()
        user.is_suspended = False
        user.save()

        # Log the action
        AdminLog.objects.create(
            admin=request.user,
            action_type=AdminLog.ActionType.USER_ACTIVATED,
            object_type='user',
            object_id=user.id,
            details={'username': user.username, 'email': user.email}
        )

        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def change_role(self, request, pk=None):
        """Change user role (guest/host/admin)"""
        user = self.get_object()
        serializer = UserRoleChangeSerializer(user, data=request.data)
        if serializer.is_valid():
            old_role = user.role
            updated_user = serializer.save()

            # Log the action
            AdminLog.objects.create(
                admin=request.user,
                action_type=AdminLog.ActionType.USER_ROLE_CHANGED,
                object_type='user',
                object_id=user.id,
                details={'username': user.username, 'old_role': old_role, 'new_role': updated_user.role}
            )

            response_serializer = self.get_serializer(updated_user)
            return Response(response_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminLogViewSet(viewsets.ReadOnlyModelViewSet):
    """View admin activity logs"""
    queryset = AdminLog.objects.all()
    serializer_class = AdminLogSerializer
    permission_classes = (IsAuthenticated, IsAdmin)

    def get_queryset(self):
        queryset = AdminLog.objects.all()
        
        # Filter by action type if provided
        action_type = self.request.query_params.get('action_type')
        if action_type:
            queryset = queryset.filter(action_type=action_type)
        
        # Filter by object type if provided
        object_type = self.request.query_params.get('object_type')
        if object_type:
            queryset = queryset.filter(object_type=object_type)
        
        return queryset.order_by('-created_at')
