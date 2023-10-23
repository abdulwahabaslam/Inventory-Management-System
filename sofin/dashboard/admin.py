from django.contrib import admin
from .models import Product, Order, InventoryMetrics, Equipment
from django.contrib.auth.models import Group

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'quantity', 'cost_per_unit')
    list_filter = ['category']

# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(InventoryMetrics)
admin.site.register(Equipment)
# UnRegister your models here.
admin.site.unregister(Group)