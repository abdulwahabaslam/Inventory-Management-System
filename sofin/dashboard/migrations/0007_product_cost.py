# Generated by Django 4.2.5 on 2023-10-10 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_inventorymetrics'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='cost',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]