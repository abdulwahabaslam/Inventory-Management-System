from django import forms
from .models import Product, Order, Equipment

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'quantity', 'cost_per_unit', 'holding_cost', 'obs_cost']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['product', 'order_quantity']

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['name', 'description', 'purchase_date', 'price', 'quantity', 'category', 'maintenance_date']