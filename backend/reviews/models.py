from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

class Review(models.Model):
    class ModerationStatus(models.TextChoices):
        CLEAN = 'clean', 'Clean'
        REPORTED = 'reported', 'Reported'
        HIDDEN = 'hidden', 'Hidden'
        RESOLVED = 'resolved', 'Resolved'

    guest = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    property = models.ForeignKey(
        'properties.Property',
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    booking = models.OneToOneField(
        'bookings.Booking',
        on_delete=models.SET_NULL,
        related_name='review',
        blank=True,
        null=True,
    )
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    moderation_status = models.CharField(
        max_length=20,
        choices=ModerationStatus.choices,
        default=ModerationStatus.CLEAN,
    )
    moderation_note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('guest', 'property')

    def __str__(self):
        return f'{self.property} - {self.rating}'
