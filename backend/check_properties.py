import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aelithrastay.settings')
django.setup()

from properties.models import Property

properties = Property.objects.all()
print(f"Total Properties: {len(properties)}")
for p in properties:
    print(f"ID: {p.id}, Title: {p.title}, Image Count: {p.images.count()}")
