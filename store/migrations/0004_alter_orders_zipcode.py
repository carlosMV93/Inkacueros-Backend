# Generated by Django 5.0.6 on 2024-06-17 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_orderitem_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='Zipcode',
            field=models.CharField(max_length=60),
        ),
    ]
