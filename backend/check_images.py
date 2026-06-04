import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aelithrastay.settings')
django.setup()

from properties.models import PropertyImage

images = PropertyImage.objects.all()
print(f"Total PropertyImage objects: {len(images)}")
for img in images:
    print(f"ID: {img.id}, Property: {img.property.title}, Image Path: {img.image.name}, URL: {img.image.url}")
