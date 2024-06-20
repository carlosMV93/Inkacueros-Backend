from django.db import models
from django.contrib.auth.models import User


class Type(models.Model):
    Name = models.CharField(max_length=30, default="")

    class Meta:
        db_table = "type"


class Brand(models.Model):
    Name = models.CharField(max_length=20)

    class Meta:
        db_table = "brand"


class Orders(models.Model):
    Delivery_Fee = models.CharField(max_length=50)
    Order_Date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    Order_Status = models.CharField(max_length=50)
    address1 = models.CharField(max_length=50)
    address2 = models.CharField(max_length=50)
    City = models.CharField(max_length=50)
    Country = models.CharField(max_length=50)
    Name = models.CharField(max_length=50)
    State = models.CharField(max_length=50)
    Zipcode = models.CharField(max_length=70)
    Sub_Total = models.FloatField()

    class Meta:
        db_table = "tb_orders"


class Products(models.Model):
    Name = models.CharField(max_length=50, default="")
    Description = models.CharField(max_length=255, default="")
    Price = models.IntegerField(default=0)
    PictureUrl = models.CharField(max_length=70, default="")
    IdType = models.ForeignKey(Type, on_delete=models.CASCADE)
    IdBrand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    class Meta:
        db_table = "tb_products"


class OrderItem(models.Model):
    Name = models.CharField(max_length=50, default="")
    Description = models.CharField(max_length=255, default="")
    Price = models.IntegerField(default=0)
    PictureUrl = models.CharField(max_length=70, default="")
    IdProduct = models.ForeignKey(Products, on_delete=models.CASCADE)
    IdOrder = models.ForeignKey(Orders, on_delete=models.CASCADE)
    IdUser = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "tb_orderitem"
