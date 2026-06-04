import builtins

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        CONFIRMED = 'confirmed', 'Confirmed'
        CANCELLED = 'cancelled', 'Cancelled'
        COMPLETED = 'completed', 'Completed'

    class DisputeStatus(models.TextChoices):
        NONE = 'none', 'None'
        OPEN = 'open', 'Open'
        REVIEWING = 'reviewing', 'Reviewing'
        RESOLVED = 'resolved', 'Resolved'

    guest = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings',
    )
    property = models.ForeignKey(
        'properties.Property',
        on_delete=models.CASCADE,
        related_name='bookings',
    )
    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    dispute_status = models.CharField(
        max_length=20,
        choices=DisputeStatus.choices,
        default=DisputeStatus.NONE,
    )
    dispute_reason = models.TextField(blank=True)
    dispute_resolution = models.TextField(blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def clean(self):
        if self.check_out <= self.check_in:
            raise ValidationError('Check-out must be after check-in.')
        if self.property_id and self.guests > self.property.max_guests:
            raise ValidationError('Guests exceed the property maximum.')

    @builtins.property
    def nights(self):
        return (self.check_out - self.check_in).days

    def calculate_total(self):
        if not self.property_id or not self.check_in or not self.check_out:
            return 0
        return (self.property.price_per_night * self.nights) + self.property.cleaning_fee

    def save(self, *args, **kwargs):
        self.total_price = self.calculate_total()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.guest} - {self.property}'
