import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aelithrastay.settings')
django.setup()

from accounts.models import User
from properties.models import Property, Amenity, PropertyImage
from decimal import Decimal

def seed():
    print("Seeding data...")
    
    # 1. Get or create a host
    host = User.objects.filter(role='host').first()
    if not host:
        host = User.objects.create_user(
            username='sample_host',
            email='host@example.com',
            password='password123',
            role='host',
            first_name='Sample',
            last_name='Host'
        )
        print(f"Created sample host: {host.username}")
    else:
        print(f"Using existing host: {host.username}")

    # 2. Create Amenities
    amenities_data = [
        {'name': 'Pool', 'icon': 'pool'},
        {'name': 'Beach access', 'icon': 'beach_access'},
        {'name': 'Wifi', 'icon': 'wifi'},
        {'name': 'Kitchen', 'icon': 'kitchen'},
        {'name': 'Free parking', 'icon': 'local_parking'},
        {'name': 'Air conditioning', 'icon': 'ac_unit'},
        {'name': 'Dedicated workspace', 'icon': 'laptop_mac'},
    ]
    
    amenities = []
    for data in amenities_data:
        amenity, created = Amenity.objects.get_or_create(name=data['name'], defaults={'icon': data['icon']})
        amenities.append(amenity)
        if created:
            print(f"Created amenity: {amenity.name}")

    # 3. Create Properties
    properties_data = [
        {
            'title': 'Luxury Villa with Private Pool',
            'description': 'A stunning 5-bedroom villa with a private infinity pool and breathtaking ocean views.',
            'property_type': 'villa',
            'address': '123 Villa Way',
            'city': 'Malibu',
            'country': 'USA',
            'price_per_night': Decimal('550.00'),
            'max_guests': 10,
            'bedrooms': 5,
            'beds': 6,
            'bathrooms': Decimal('4.5'),
        },
        {
            'title': 'Cozy Mountain Cabin',
            'description': 'Rustic cabin nestled in the woods, perfect for a quiet getaway. Features a stone fireplace.',
            'property_type': 'cabin',
            'address': '456 Pine Trail',
            'city': 'Aspen',
            'country': 'USA',
            'price_per_night': Decimal('120.00'),
            'max_guests': 4,
            'bedrooms': 2,
            'beds': 2,
            'bathrooms': Decimal('1.0'),
        },
        {
            'title': 'Modern City Apartment',
            'description': 'Sleek and stylish apartment in the heart of the city, close to all major attractions.',
            'property_type': 'apartment',
            'address': '789 Metro Ave',
            'city': 'Paris',
            'country': 'France',
            'price_per_night': Decimal('200.00'),
            'max_guests': 2,
            'bedrooms': 1,
            'beds': 1,
            'bathrooms': Decimal('1.0'),
        },
        {
            'title': 'Santorini Cliffside Suite',
            'description': 'Traditional blue and white suite with a private hot tub overlooking the caldera.',
            'property_type': 'apartment',
            'address': '10 Caldera View',
            'city': 'Oia',
            'country': 'Greece',
            'price_per_night': Decimal('450.00'),
            'max_guests': 2,
            'bedrooms': 1,
            'beds': 1,
            'bathrooms': Decimal('1.0'),
        }
    ]

    for p_data in properties_data:
        prop, created = Property.objects.get_or_create(
            title=p_data['title'],
            host=host,
            defaults=p_data
        )
        if created:
            # Add some random amenities
            import random
            prop.amenities.add(*random.sample(amenities, k=min(len(amenities), 4)))
            print(f"Created property: {prop.title}")
            
            # Since we don't have actual files, the frontend fallback logic will handle images 
            # if we don't create PropertyImage objects or if they don't have files.
            # But let's create one dummy image record to see if it works.
            # However, without an actual file on disk, the URL might be broken.
            # The frontend has fallback images which is better for now.

    print("Seeding complete!")

if __name__ == '__main__':
    seed()
