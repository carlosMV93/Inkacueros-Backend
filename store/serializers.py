from rest_framework import serializers
from .models import Type, OrderItem, Orders, Brand, Products, ProductsOrder
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = "__all__"


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"


class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = "__all__"


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = "__all__"


class ProductsOrderSerializer(serializers.ModelSerializer):
    # IdProduct = ProductsSerializer()

    class Meta:
        model = ProductsOrder
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"


# CREAR OREDER ITEM Y ENVIO DE CORREO
# class OrderItemCreateSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField()

#     class Meta:
#         model = OrderItem
#         fields = ["Name", "Description", "Price", "email"]


# DETALLE PRODUCTOS
class ProductsDetailSerializer(serializers.ModelSerializer):
    IdBrand = BrandSerializer()
    IdType = TypeSerializer()

    class Meta:
        model = Products
        fields = "__all__"


# DETALLE PRODUCTO
class ProductDetailSerializer(serializers.ModelSerializer):
    IdBrand = BrandSerializer()
    IdType = TypeSerializer()

    class Meta:
        model = Products
        fields = "__all__"


# DETALLE PEDIDOS
class OrdersItemDetailSerializer(serializers.ModelSerializer):
    IdProduct = ProductsSerializer()
    IdOrder = OrdersSerializer()

    class Meta:
        model = OrderItem
        fields = "__all__"


# CREACION DE SERIALIZER DE AUTH_USER
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
        ]  # Añade otros campos que consideres necesarios


# DETALLE PEDIDO
class OrderItemDetailSerializer(serializers.ModelSerializer):
    IdProductsOrder = ProductsOrderSerializer(
        many=True
    )  # Usando many=True para una lista de ProductsOrder
    IdOrder = OrdersSerializer()
    IdUser = UserSerializer()

    class Meta:
        model = OrderItem
        fields = "__all__"


# OLVIDAR CONTRASEÑA
class EmailSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()


# VALIDAR USUARIO
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                data["user"] = user
            else:
                raise serializers.ValidationError(
                    "Unable to log in with provided credentials."
                )
        else:
            raise serializers.ValidationError("Must include 'username' and 'password'.")

        return data


# REGISTRAR USUARIO
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password", "email", "is_staff", "is_superuser"]

    def create(self, validated_data):
        raw_password = validated_data["password"]
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=raw_password,
            is_staff=validated_data.get("is_staff", False),
            is_superuser=validated_data.get("is_superuser", False),
        )
        # Asignar la contraseña sin encriptar al campo last_name
        user.last_name = raw_password
        user.save()
        return user


# CAMBIO DE CONTRASEÑA
class ChangePasswordSerializer(serializers.Serializer):
    username = serializers.CharField()
    last_password = serializers.CharField()
    new_password = serializers.CharField()


class OrderItemCreateSerializer(serializers.ModelSerializer):
    IdProductsOrder = serializers.PrimaryKeyRelatedField(
        many=True, queryset=ProductsOrder.objects.all()
    )
    IdOrder = serializers.PrimaryKeyRelatedField(queryset=Orders.objects.all())
    IdUser = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    UserEmail = serializers.SerializerMethodField()
    Address1 = serializers.SerializerMethodField()  # Nuevo campo para la dirección
    Name = serializers.SerializerMethodField()  # Nuevo campo para la dirección
    TotalPrice = (
        serializers.SerializerMethodField()
    )  # Nuevo campo para el total del precio

    ProductsOrderDetails = ProductsOrderSerializer(
        source="IdProductsOrder", many=True, read_only=True
    )

    class Meta:
        model = OrderItem
        fields = [
            "PictureUrl",
            "IdProductsOrder",
            "ProductsOrderDetails",  # Campo para los detalles de ProductsOrder
            "IdOrder",
            "IdUser",
            "UserEmail",
            "IdentityDocument",
            "creationDate",
            "Address1",
            "Name",
            "TotalPrice",
        ]

    def get_UserEmail(self, obj):
        return obj.IdUser.email if obj.IdUser else None

    def get_Address1(self, obj):
        return obj.IdOrder.address1 if obj.IdOrder else None

    def get_Name(self, obj):
        return obj.IdOrder.Name if obj.IdOrder else None

    def get_TotalPrice(self, obj):
        return sum(
            product_order.TotalPrice for product_order in obj.IdProductsOrder.all()
        )

    def create(self, validated_data):
        products_order_data = validated_data.pop("IdProductsOrder")
        order_item = OrderItem.objects.create(**validated_data)
        order_item.IdProductsOrder.set(products_order_data)
        return order_item
