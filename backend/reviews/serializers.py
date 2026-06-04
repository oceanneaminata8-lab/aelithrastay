from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    guest = serializers.HiddenField(default=serializers.CurrentUserDefault())
    guest_name = serializers.StringRelatedField(source='guest', read_only=True)
    property_title = serializers.CharField(source='property.title', read_only=True)

    class Meta:
        model = Review
        fields = (
            'id',
            'guest',
            'guest_name',
            'property',
            'property_title',
            'booking',
            'rating',
            'comment',
            'moderation_status',
            'moderation_note',
            'created_at',
        )
        read_only_fields = ('id', 'guest_name', 'created_at')
        extra_kwargs = {
            'booking': {'required': False, 'allow_null': True}
        }
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['guest', 'property'],
                message="You have already reviewed this property."
            )
        ]
