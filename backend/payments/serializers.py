from rest_framework import serializers

from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    booking_total = serializers.DecimalField(
        source='booking.total_price',
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )

    class Meta:
        model = Payment
        fields = (
            'id',
            'booking',
            'booking_total',
            'amount',
            'method',
            'status',
            'transaction_reference',
            'paid_at',
            'created_at',
        )
        read_only_fields = ('id', 'amount', 'created_at')
