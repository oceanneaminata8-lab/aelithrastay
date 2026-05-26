from rest_framework import serializers

from properties.serializers import PropertySerializer
from .models import Wishlist


class WishlistSerializer(serializers.ModelSerializer):
    property_detail = PropertySerializer(source='property', read_only=True)

    class Meta:
        model = Wishlist
        fields = ('id', 'property', 'property_detail', 'created_at')
        read_only_fields = ('id', 'created_at')
