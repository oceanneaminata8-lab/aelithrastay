from rest_framework import serializers

from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    guest = serializers.StringRelatedField(read_only=True)
    property_title = serializers.CharField(source='property.title', read_only=True)
    host_id = serializers.IntegerField(source='property.host.id', read_only=True)
    nights = serializers.IntegerField(read_only=True)

    class Meta:
        model = Booking
        fields = (
            'id',
            'guest',
            'property',
            'property_title',
            'host_id',
            'check_in',
            'check_out',
            'guests',
            'nights',
            'status',
            'dispute_status',
            'dispute_reason',
            'dispute_resolution',
            'total_price',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'guest', 'total_price', 'created_at', 'updated_at')

    def validate(self, attrs):
        instance = self.instance
        property_obj = attrs.get('property') or getattr(instance, 'property', None)
        check_in = attrs.get('check_in') or getattr(instance, 'check_in', None)
        check_out = attrs.get('check_out') or getattr(instance, 'check_out', None)
        guests = attrs.get('guests') or getattr(instance, 'guests', None)

        if check_in and check_out and check_out <= check_in:
            raise serializers.ValidationError('Check-out must be after check-in.')
        if property_obj and guests and guests > property_obj.max_guests:
            raise serializers.ValidationError('Guests exceed the property maximum.')

        if property_obj and check_in and check_out:
            overlapping = Booking.objects.filter(
                property=property_obj,
                check_in__lt=check_out,
                check_out__gt=check_in,
            ).exclude(status=Booking.Status.CANCELLED)
            if instance:
                overlapping = overlapping.exclude(pk=instance.pk)
            if overlapping.exists():
                raise serializers.ValidationError('This property is already booked for those dates.')

        return attrs
