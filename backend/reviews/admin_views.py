from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from aelithrastay.permissions import IsAdmin
from accounts.models import AdminLog
from .models import Review
from .serializers import ReviewSerializer


class AdminReviewModerationViewSet(viewsets.ReadOnlyModelViewSet):
    """Admin endpoint for managing review moderation"""
    permission_classes = (IsAuthenticated, IsAdmin)
    serializer_class = ReviewSerializer

    def get_queryset(self):
        # Show all reviews for moderation purposes
        queryset = Review.objects.select_related('guest', 'property', 'booking')
        
        # Filter by status if provided
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(moderation_status=status_filter)
        else:
            # By default show reported and problematic reviews
            queryset = queryset.filter(moderation_status__in=[
                Review.ModerationStatus.REPORTED,
                Review.ModerationStatus.CLEAN,
            ])
        
        return queryset.order_by('-created_at')

    @action(detail=True, methods=['post'])
    def hide(self, request, pk=None):
        """Hide a review from public view"""
        review = self.get_object()
        review.moderation_status = Review.ModerationStatus.HIDDEN
        review.moderation_note = request.data.get('note', '')
        review.save()

        AdminLog.objects.create(
            admin=request.user,
            action_type=AdminLog.ActionType.REVIEW_HIDDEN,
            object_type='review',
            object_id=review.id,
            details={
                'property': review.property.title,
                'reviewer': review.guest.username,
                'reason': review.moderation_note
            }
        )

        serializer = self.get_serializer(review)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def mark_reported(self, request, pk=None):
        """Mark a review as reported"""
        review = self.get_object()
        review.moderation_status = Review.ModerationStatus.REPORTED
        review.save()

        AdminLog.objects.create(
            admin=request.user,
            action_type=AdminLog.ActionType.REVIEW_REPORTED,
            object_type='review',
            object_id=review.id,
            details={'property': review.property.title, 'reviewer': review.guest.username}
        )

        serializer = self.get_serializer(review)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        """Resolve a reported review"""
        review = self.get_object()
        review.moderation_status = Review.ModerationStatus.RESOLVED
        review.moderation_note = request.data.get('resolution', '')
        review.save()

        AdminLog.objects.create(
            admin=request.user,
            action_type=AdminLog.ActionType.REVIEW_RESOLVED,
            object_type='review',
            object_id=review.id,
            details={
                'property': review.property.title,
                'reviewer': review.guest.username,
                'resolution': review.moderation_note
            }
        )

        serializer = self.get_serializer(review)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get review moderation statistics"""
        from django.db.models import Count
        stats = Review.objects.values('moderation_status').annotate(count=Count('id'))
        return Response(stats)
