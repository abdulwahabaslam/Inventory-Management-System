# Generated by Django 4.2.5 on 2023-10-08 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_alter_order_options_alter_product_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='reporting_period',
            field=models.DateField(null=True),
        ),
    ]