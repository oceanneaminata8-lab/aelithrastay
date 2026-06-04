from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from aelithrastay.permissions import IsAdmin
from accounts.models import AdminLog
from .models import Property
from .serializers import PropertySerializer


class AdminPropertyApprovalViewSet(viewsets.ReadOnlyModelViewSet):
    """Admin endpoint for property approval and reporting"""
    permission_classes = (IsAuthenticated, IsAdmin)
    serializer_class = PropertySerializer

    def get_queryset(self):
        queryset = Property.objects.select_related('host').prefetch_related('amenities', 'images', 'reviews')
        
        # Filter by status if provided
        status_filter = self.request.query_params.get('approval_status')
        if status_filter:
            queryset = queryset.filter(approval_status=status_filter)
        else:
            # By default show pending properties
            queryset = queryset.filter(approval_status=Property.ApprovalStatus.PENDING)
        
        # Show reported properties
        show_reported = self.request.query_params.get('reported')
        if show_reported == 'true':
            queryset = queryset.filter(is_reported=True)
        
        return queryset.order_by('-created_at')

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve a property listing"""
        property_obj = self.get_object()
        property_obj.approval_status = Property.ApprovalStatus.APPROVED
        property_obj.is_reported = False
        property_obj.moderation_note = request.data.get('note', '')
        property_obj.save()

        AdminLog.objects.create(
            admin=request.user,
            action_type=AdminLog.ActionType.PROPERTY_APPROVED,
            object_type='property',
            object_id=property_obj.id,
            details={'title': property_obj.title, 'host': property_obj.host.username}
        )

        serializer = self.get_serializer(property_obj)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Reject a property listing"""
        property_obj = self.get_object()
        property_obj.approval_status = Property.ApprovalStatus.REJECTED
        property_obj.moderation_note = request.data.get('reason', '')
        property_obj.save()

        AdminLog.objects.create(
            admin=request.user,
            action_type=AdminLog.ActionType.PROPERTY_REJECTED,
            object_type='property',
            object_id=property_obj.id,
            details={
                'title': property_obj.title,
                'host': property_obj.host.username,
                'reason': property_obj.moderation_note
            }
        )

        serializer = self.get_serializer(property_obj)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def mark_reported(self, request, pk=None):
        """Mark a property as reported"""
        property_obj = self.get_object()
        property_obj.is_reported = True
        property_obj.moderation_note = request.data.get('report_reason', '')
        property_obj.save()

        AdminLog.objects.create(
            admin=request.user,
            action_type=AdminLog.ActionType.PROPERTY_REPORTED,
            object_type='property',
            object_id=property_obj.id,
            details={
                'title': property_obj.title,
                'host': property_obj.host.username,
                'reason': property_obj.moderation_note
            }
        )

        serializer = self.get_serializer(property_obj)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def resolve_report(self, request, pk=None):
        """Resolve a reported property"""
        property_obj = self.get_object()
        property_obj.is_reported = False
        property_obj.moderation_note = request.data.get('resolution', '')
        property_obj.save()

        AdminLog.objects.create(
            admin=request.user,
            action_type=AdminLog.ActionType.PROPERTY_REPORTED_RESOLVED,
            object_type='property',
            object_id=property_obj.id,
            details={
                'title': property_obj.title,
                'host': property_obj.host.username,
                'resolution': property_obj.moderation_note
            }
        )

        serializer = self.get_serializer(property_obj)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get property moderation statistics"""
        from django.db.models import Count
        approval_stats = Property.objects.values('approval_status').annotate(count=Count('id'))
        reported_count = Property.objects.filter(is_reported=True).count()
        return Response({
            'by_approval_status': list(approval_stats),
            'reported_count': reported_count
        })
