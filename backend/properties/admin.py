from django.contrib import admin

from .models import Amenity, Property, PropertyImage


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    inlines = (PropertyImageInline,)
    list_display = ('title', 'host', 'city', 'country', 'price_per_night', 'is_active')
    list_filter = ('property_type', 'city', 'country', 'is_active')
    search_fields = ('title', 'description', 'city', 'country', 'host__username')
    filter_horizontal = ('amenities',)


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ('property', 'caption', 'is_cover', 'created_at')
