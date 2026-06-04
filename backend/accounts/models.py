from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
    class Role(models.TextChoices):
        GUEST = 'guest', 'Guest'
        HOST = 'host', 'Host'
        ADMIN = 'admin', 'Admin'

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.GUEST)
    phone = models.CharField(max_length=30, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True)
    is_suspended = models.BooleanField(default=False)

    def __str__(self):
        return self.get_full_name() or self.username


class AdminLog(models.Model):
    class ActionType(models.TextChoices):
        USER_SUSPENDED = 'user_suspended', 'User Suspended'
        USER_ACTIVATED = 'user_activated', 'User Activated'
        USER_ROLE_CHANGED = 'user_role_changed', 'User Role Changed'
        PROPERTY_APPROVED = 'property_approved', 'Property Approved'
        PROPERTY_REJECTED = 'property_rejected', 'Property Rejected'
        PROPERTY_REPORTED = 'property_reported', 'Property Reported'
        PROPERTY_REPORTED_RESOLVED = 'property_reported_resolved', 'Property Report Resolved'
        REVIEW_HIDDEN = 'review_hidden', 'Review Hidden'
        REVIEW_REPORTED = 'review_reported', 'Review Reported'
        REVIEW_RESOLVED = 'review_resolved', 'Review Resolved'
        DISPUTE_OPENED = 'dispute_opened', 'Dispute Opened'
        DISPUTE_REVIEWING = 'dispute_reviewing', 'Dispute Under Review'
        DISPUTE_RESOLVED = 'dispute_resolved', 'Dispute Resolved'
        PAYMENT_REFUNDED = 'payment_refunded', 'Payment Refunded'

    admin = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='admin_logs',
    )
    action_type = models.CharField(max_length=50, choices=ActionType.choices)
    object_type = models.CharField(max_length=50)  # user, property, review, booking, payment
    object_id = models.PositiveIntegerField()
    details = models.JSONField(default=dict, blank=True)  # Additional details about the action
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.admin.username} - {self.action_type} - {self.object_type}({self.object_id})'
