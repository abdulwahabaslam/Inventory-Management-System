# Generated by Django 4.2.5 on 2023-10-12 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0010_product_cogs_product_holding_cost'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='obs_cost',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True),
        ),
    ]
