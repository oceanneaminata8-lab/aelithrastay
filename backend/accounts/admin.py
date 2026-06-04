from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('AelithraStay profile', {'fields': ('role', 'phone', 'avatar', 'bio', 'is_suspended')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_suspended', 'is_staff')
    list_filter = UserAdmin.list_filter + ('role', 'is_suspended')
