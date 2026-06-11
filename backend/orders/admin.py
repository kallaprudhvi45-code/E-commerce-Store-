from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'total_price', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('order_id',)
