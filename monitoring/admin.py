from django.contrib import admin
from payments.models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("user", "levy", "amount", "month", "verified")
    list_filter = ("levy", "month")
    search_fields = ("user__full_name", "reference")
