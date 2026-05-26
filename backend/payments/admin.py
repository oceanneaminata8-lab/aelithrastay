from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('booking', 'amount', 'method', 'status', 'transaction_reference', 'created_at')
    list_filter = ('status', 'method', 'created_at')
    search_fields = ('booking__property__title', 'booking__guest__username', 'transaction_reference')
