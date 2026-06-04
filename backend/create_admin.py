import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aelithrastay.settings')
django.setup()

from accounts.models import User


ADMIN_EMAIL = 'admin@aelithrastay.com'
ADMIN_PASSWORD = 'Admin@12345'


def run():
    user = User.objects.filter(email=ADMIN_EMAIL).first() or User.objects.filter(username='admin').first()
    if not user:
        user = User(username='admin', email=ADMIN_EMAIL)

    user.email = ADMIN_EMAIL
    user.first_name = user.first_name or 'AelithraStay'
    user.last_name = user.last_name or 'Admin'
    user.role = User.Role.ADMIN
    user.is_staff = True
    user.is_superuser = True
    user.is_suspended = False
    user.set_password(ADMIN_PASSWORD)
    user.save()
    print(f'Admin ready: {ADMIN_EMAIL} / {ADMIN_PASSWORD}')


if __name__ == '__main__':
    run()
