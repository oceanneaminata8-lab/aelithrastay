from rest_framework import permissions, viewsets

from aelithrastay.permissions import IsHostOrReadOnly, IsPropertyHostOrReadOnly
from .models import Amenity, Property, PropertyImage
from .serializers import AmenitySerializer, PropertyImageSerializer, PropertySerializer


class AmenityViewSet(viewsets.ModelViewSet):
    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer
    permission_classes = (IsHostOrReadOnly,)


class PropertyViewSet(viewsets.ModelViewSet):
    serializer_class = PropertySerializer
    permission_classes = (IsHostOrReadOnly, IsPropertyHostOrReadOnly)
    search_fields = ('title', 'description', 'city', 'country', 'address')
    ordering_fields = ('price_per_night', 'created_at', 'max_guests', 'bedrooms')
    ordering = ('-created_at',)

    def get_queryset(self):
        queryset = Property.objects.select_related('host').prefetch_related(
            'amenities',
            'images',
            'reviews',
        )
        user = self.request.user
        if not (user.is_authenticated and (user.is_staff or user.role == 'admin')):
            queryset = queryset.filter(is_active=True, approval_status=Property.ApprovalStatus.APPROVED)

        city = self.request.query_params.get('city')
        country = self.request.query_params.get('country')
        property_type = self.request.query_params.get('property_type')
        guests = self.request.query_params.get('guests')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        mine = self.request.query_params.get('mine')

        if city:
            queryset = queryset.filter(city__icontains=city)
        if country:
            queryset = queryset.filter(country__icontains=country)
        if property_type:
            queryset = queryset.filter(property_type=property_type)
        if guests:
            queryset = queryset.filter(max_guests__gte=guests)
        if min_price:
            queryset = queryset.filter(price_per_night__gte=min_price)
        if max_price:
            queryset = queryset.filter(price_per_night__lte=max_price)
        if mine == 'true' and user.is_authenticated:
            queryset = queryset.filter(host=user)

        return queryset

    def perform_create(self, serializer):
        approval_status = Property.ApprovalStatus.APPROVED if (
            self.request.user.is_staff or self.request.user.role == 'admin'
        ) else Property.ApprovalStatus.PENDING
        serializer.save(host=self.request.user, approval_status=approval_status)


class PropertyImageViewSet(viewsets.ModelViewSet):
    serializer_class = PropertyImageSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        queryset = PropertyImage.objects.select_related('property', 'property__host')
        if user.is_staff or user.role == 'admin':
            return queryset
        return queryset.filter(property__host=user)

    def perform_create(self, serializer):
        property_obj = serializer.validated_data['property']
        if not (self.request.user.is_staff or self.request.user.role == 'admin' or property_obj.host_id == self.request.user.id):
            self.permission_denied(self.request)
        serializer.save()
