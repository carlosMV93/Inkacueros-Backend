# Generated by Django 5.0.6 on 2024-06-20 01:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_alter_orders_zipcode'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='IdUser',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='IdOrder',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='store.orders'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='IdProduct',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='store.products'),
        ),
    ]
