from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from properties.serializers import PropertySerializer
from .models import Wishlist


class WishlistSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    property_detail = PropertySerializer(source='property', read_only=True)

    class Meta:
        model = Wishlist
        fields = ('id', 'user', 'property', 'property_detail', 'created_at')
        read_only_fields = ('id', 'created_at')
        validators = [
            UniqueTogetherValidator(
                queryset=Wishlist.objects.all(),
                fields=['user', 'property'],
                message="This property is already in your wishlist."
            )
        ]
