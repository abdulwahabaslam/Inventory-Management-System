# Generated by Django 4.2.5 on 2023-10-08 20:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_order_reporting_period'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='reporting_period',
        ),
    ]
