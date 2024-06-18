from django.shortcuts import render
from rest_framework import viewsets, status, permissions, generics
from .models import Type, Brand, OrderItem, Orders, Products
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth.models import User

# from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.conf import settings

from rest_framework.views import APIView
from .serializers import (
    TypeSerializer,
    BrandSerializer,
    OrderItemSerializer,
    OrdersSerializer,
    ProductsSerializer,
    UserLoginSerializer,
    UserSerializer,
    OrderItemDetailSerializer,
    ProductsDetailSerializer,
    EmailSerializer,
)


class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)


class MyTokenRefreshView(TokenRefreshView):
    permission_classes = permissions.AllowAny


class TypeViewSet(viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class OrdersViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer


class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


# DETALLE PRODUCTO
class ProductsDetailViewSet(generics.RetrieveAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductsDetailSerializer
    lookup_field = "id"


# DETALLE PRODUCTOS
class ProductsListViewSet(generics.ListAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductsDetailSerializer


# DETALLE PEDIDO
class OrderItemDetailView(generics.RetrieveAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemDetailSerializer
    lookup_field = "id"


# DETALLE PEDIDOS
class OrderItemListView(generics.ListAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemDetailSerializer


# OLVIDAR CONTRASEÑA
class SendPasswordEmailView(APIView):
    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            email = serializer.validated_data["email"]

            try:
                user = User.objects.get(username=username)
                # Create EmailMessage instance
                email_message = EmailMessage(
                    subject="Your Password",
                    body=f"Hello {username}, your password is: {user.password}",
                    from_email=settings.EMAIL_HOST_USER,
                    to=[email],
                )
                # Send email
                email_message.send()
                return Response(
                    {"message": "Email sent successfully."}, status=status.HTTP_200_OK
                )
            except User.DoesNotExist:
                return Response(
                    {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# VALIDAR USUARIO
@api_view(["POST"])
def user_login(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data["user"]
        return Response(
            {"username": user.username, "email": user.email}, status=status.HTTP_200_OK
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# REGISTRAR USUARIO
@api_view(["POST"])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
