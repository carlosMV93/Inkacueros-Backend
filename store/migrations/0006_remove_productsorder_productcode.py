# Generated by Django 5.0.6 on 2024-06-21 02:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_remove_orders_address2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productsorder',
            name='ProductCode',
        ),
    ]
