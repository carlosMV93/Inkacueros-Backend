from rest_framework import serializers
from .models import Type, OrderItem, Orders, Brand, Products
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


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderItemDetailSerializer(serializers.ModelSerializer):
    IdProduct = ProductsSerializer()
    IdOrder = OrdersSerializer()

    class Meta:
        model = OrderItem
        fields = "__all__"


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
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            is_staff=validated_data.get("is_staff", False),
            is_superuser=validated_data.get("is_superuser", False),
        )
        return user
