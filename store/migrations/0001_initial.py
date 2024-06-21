# Generated by Django 5.0.6 on 2024-06-21 01:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'brand',
            },
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Delivery_Fee', models.CharField(max_length=50)),
                ('Order_Date', models.DateTimeField(auto_now_add=True, null=True)),
                ('Order_Status', models.CharField(max_length=50)),
                ('address1', models.CharField(max_length=50)),
                ('address2', models.CharField(max_length=50)),
                ('City', models.CharField(max_length=50)),
                ('Country', models.CharField(max_length=50)),
                ('Name', models.CharField(max_length=50)),
                ('State', models.CharField(max_length=50)),
                ('Zipcode', models.CharField(max_length=70)),
                ('Sub_Total', models.FloatField()),
            ],
            options={
                'db_table': 'tb_orders',
            },
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(default='', max_length=30)),
            ],
            options={
                'db_table': 'type',
            },
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(default='', max_length=50)),
                ('Description', models.CharField(default='', max_length=255)),
                ('Price', models.IntegerField(default=0)),
                ('PictureUrl', models.CharField(default='', max_length=70)),
                ('IdBrand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.brand')),
                ('IdType', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.type')),
            ],
            options={
                'db_table': 'tb_products',
            },
        ),
        migrations.CreateModel(
            name='ProductsOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Amount', models.IntegerField(default=0)),
                ('TotalPrice', models.FloatField(default=0.0)),
                ('ProductCode', models.IntegerField(default=0)),
                ('creationDate', models.DateTimeField(default=True)),
                ('IdProduct', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='store.products')),
            ],
            options={
                'db_table': 'tb_product_order',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(default='', max_length=50)),
                ('Description', models.CharField(default='', max_length=255)),
                ('Price', models.IntegerField(default=0)),
                ('PictureUrl', models.CharField(default='', max_length=70)),
                ('IdentityDocument', models.CharField(default='', max_length=25)),
                ('StatusOrderDetail', models.CharField(default='', max_length=150)),
                ('StatusOrderEmail', models.BooleanField(default=True)),
                ('creationDate', models.DateTimeField(default=True)),
                ('IdUser', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('IdOrder', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='store.orders')),
                ('IdProductsOrder', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='store.productsorder')),
            ],
            options={
                'db_table': 'tb_orderitem',
            },
        ),
    ]
