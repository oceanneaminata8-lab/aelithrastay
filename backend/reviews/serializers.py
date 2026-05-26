from rest_framework import serializers

from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    guest = serializers.StringRelatedField(read_only=True)
    property_title = serializers.CharField(source='property.title', read_only=True)

    class Meta:
        model = Review
        fields = (
            'id',
            'guest',
            'property',
            'property_title',
            'booking',
            'rating',
            'comment',
            'created_at',
        )
        read_only_fields = ('id', 'guest', 'created_at')
        extra_kwargs = {
            'booking': {'required': False, 'allow_null': True}
        }
