from rest_framework import serializers

from .models import Amenity, Property, PropertyImage


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ('id', 'name', 'icon')


class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ('id', 'property', 'image', 'caption', 'is_cover', 'created_at')
        read_only_fields = ('id', 'created_at')


class PropertySerializer(serializers.ModelSerializer):
    host = serializers.StringRelatedField(read_only=True)
    host_id = serializers.IntegerField(source='host.id', read_only=True)
    amenities = AmenitySerializer(many=True, read_only=True)
    amenity_ids = serializers.PrimaryKeyRelatedField(
        queryset=Amenity.objects.all(),
        many=True,
        write_only=True,
        required=False,
        source='amenities',
    )
    images = PropertyImageSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    review_count = serializers.IntegerField(source='reviews.count', read_only=True)

    class Meta:
        model = Property
        fields = (
            'id',
            'host',
            'host_id',
            'title',
            'description',
            'property_type',
            'address',
            'city',
            'country',
            'latitude',
            'longitude',
            'price_per_night',
            'cleaning_fee',
            'max_guests',
            'bedrooms',
            'beds',
            'bathrooms',
            'amenities',
            'amenity_ids',
            'images',
            'average_rating',
            'review_count',
            'is_active',
            'approval_status',
            'is_reported',
            'moderation_note',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'created_at', 'updated_at')

    def get_average_rating(self, obj):
        ratings = [review.rating for review in obj.reviews.all()]
        if not ratings:
            return None
        return round(sum(ratings) / len(ratings), 1)
