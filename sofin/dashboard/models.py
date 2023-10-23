from django.db import models
from django.contrib.auth.models import User

# Create your models here.

CATEGORY = (
    ('Stationary', 'Stationary'),
    ('Electronics', 'Electronics'),
    ('Food', 'Food'),
)

EQUIPMENT_CATEGORY = (
    ('Furniture', 'Furniture'),
    ('Vehicles', 'Vehicles'),
)

class Product(models.Model):
    name = models.CharField(max_length=100, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY, null=True)
    quantity = models.PositiveIntegerField(null=True)
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    cogs = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    holding_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    obs_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)

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

    def calculate_cogs(self):
        return self.product.cost_per_unit * self.order_quantity

    class Meta:
        verbose_name_plural = 'Order'

    def __str__(self):
        return f'{self.product} ordered by {self.staff.username}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update the inventory metrics
        if self.product:
            self.order_cost = self.product.cost_per_unit * self.order_quantity
            self.product.cogs += self.calculate_cogs()
            self.product.quantity -= self.order_quantity
            self.product.save()
            super().save(*args, **kwargs)
            
class InventoryMetrics(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    turnover_rate = models.FloatField(null=True)
    date = models.DateTimeField(auto_now_add=True)

    def calculate_inventory_turnover_rate(self):
        total_cogs = Order.objects.filter(product=self.product).aggregate(total_cogs=models.Sum('order_cost'))['total_cogs'] or 0
        average_inventory = (self.product.cogs + self.product.holding_cost) / 2

        if average_inventory != 0:
            turnover_rate = total_cogs / average_inventory
        else:
            turnover_rate = 0

        return turnover_rate
    def save(self, *args, **kwargs):
        self.turnover_rate = self.calculate_inventory_turnover_rate()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.product} - Date: {self.date}'

    class Meta:
        verbose_name_plural = 'Inventory Metrics'

class Equipment(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    purchase_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    category = models.CharField(max_length=20, choices=EQUIPMENT_CATEGORY, null=True)

    def __str__(self):
        return f'{self.name}-{self.category}'
