from django.db import models
from django.contrib.auth.models import User


class Type(models.Model):
    Name = models.CharField(max_length=30, default="")

    class Meta:
        db_table = "type"


class Brand(models.Model):
    Name = models.CharField(max_length=21)

    class Meta:
        db_table = "brand"


class Orders(models.Model):
    Delivery_Fee = models.CharField(max_length=51)
    Order_Date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    Order_Status = models.CharField(max_length=50)
    address1 = models.CharField(max_length=50)
    City = models.CharField(max_length=50)
    Country = models.CharField(max_length=50)
    Name = models.CharField(max_length=50)
    State = models.CharField(max_length=50)
    Zipcode = models.CharField(max_length=70)

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


class ProductsOrder(models.Model):
    Amount = models.IntegerField(default=0)
    TotalPrice = models.FloatField(default=0.00)
    creationDate = models.DateTimeField(default=True)
    IdProduct = models.ForeignKey(Products, on_delete=models.CASCADE, default=0)

    class Meta:
        db_table = "tb_product_order"


class OrderItem(models.Model):
    PictureUrl = models.CharField(max_length=70, default="")
    IdProductsOrder = models.ManyToManyField(ProductsOrder)
    IdOrder = models.ForeignKey(Orders, on_delete=models.CASCADE, default=0)
    IdUser = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    # ORDERS TABLE -ADMIN
    IdentityDocument = models.CharField(max_length=25, default="")
    StatusOrderDetail = models.CharField(
        max_length=150, default="Llego el correo , se valido"
    )
    StatusOrderEmail = models.BooleanField(default=True)
    creationDate = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        db_table = "tb_orderitem"
