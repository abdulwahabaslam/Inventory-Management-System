from django.db import models
from django.contrib.auth.models import User

# Create your models here.

CATEGORY = (
    ('Stationary', 'Stationary'),
    ('Electronics', 'Electronics'),
    ('Food', 'Food'),
)

class Product(models.Model):
    name = models.CharField(max_length=100, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY, null=True)
    quantity = models.PositiveIntegerField(null=True)
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    def __str__(self):
        return f'{self.name}-{self.quantity}'

    class Meta:
        verbose_name_plural = 'Product'

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    staff = models.ForeignKey(User, on_delete=models.CASCADE, null= True)
    order_quantity = models.PositiveIntegerField(null=True)
    date = models.DateTimeField(auto_now_add=True)
    order_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    class Meta:
        verbose_name_plural = 'Order'

    def __str__(self):
        return f'{self.product} ordered by {self.staff.username}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update the inventory metrics
        if self.product:
            self.order_cost = self.product.cost_per_unit * self.order_quantity
            super().save(*args, **kwargs)
            
class InventoryMetrics(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    turnover_rate = models.FloatField(null=True)
    holding_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    obsolescence_risks = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product} - Date: {self.date}'

    class Meta:
        verbose_name_plural = 'Inventory Metrics'