from django.shortcuts import render
from rest_framework import viewsets, status, permissions, generics
from .models import Type, Brand, OrderItem, Orders, Products, ProductsOrder
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, timedelta

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
    ChangePasswordSerializer,
    OrderItemCreateSerializer,
    ProductsOrderSerializer,
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


class ProductsOrdersViewSet(viewsets.ModelViewSet):
    queryset = ProductsOrder.objects.all()
    serializer_class = ProductsOrderSerializer


# class OrderItemViewSet(viewsets.ModelViewSet):
#     queryset = OrderItem.objects.all()
#     serializer_class = OrderItemSerializer


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
            {
                "username": user.username,
                "email": user.email,
                "admin": user.is_superuser,
                "idUser": user.id,
            },
            status=status.HTTP_200_OK,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# REGISTRAR USUARIO
@api_view(["POST"])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()

        # Enviar correo electrónico
        subject = "BIENVENIDO A LA FAMILIA INKACUEROS"
        html_message = render_to_string(
            "welcome_email.html", {"username": user.username, "email": user.email}
        )
        email = EmailMessage(subject, html_message, "tu_email@gmail.com", [user.email])
        email.content_subtype = "html"
        email.send()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# CAMBIO DE CONTRASEÑA
class ChangePasswordView(APIView):
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            last_password = serializer.validated_data["last_password"]
            new_password = serializer.validated_data["new_password"]

            try:
                user = User.objects.get(username=username, last_name=last_password)
                user.last_name = new_password
                user.set_password(new_password)
                user.save()

                return Response(
                    {"message": "Password updated successfully"},
                    status=status.HTTP_200_OK,
                )

            except User.DoesNotExist:
                return Response(
                    {"username": ["User not found."]}, status=status.HTTP_404_NOT_FOUND
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# CREACIÓN DE ORDERITEM Y ENVIO DE CORREO
class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = OrderItemCreateSerializer(data=request.data)
        if serializer.is_valid():
            order_item = serializer.save()

            # Obtener los detalles de ProductsOrder del serializer data
            products_order_details = serializer.data.get("ProductsOrderDetails", None)
            if products_order_details:
                # Lista para almacenar los detalles de productos para el correo electrónico
                products_details_for_email = []

                for product_order in products_order_details:
                    id_product = product_order.get("IdProduct", None)
                    amount = product_order.get("Amount", None)
                    total_price = product_order.get("TotalPrice", None)
                    if id_product:
                        try:
                            # Buscar el producto usando el id_product
                            product = Products.objects.get(pk=id_product)

                            # Añadir detalles del producto al contexto para el correo electrónico
                            product_details = {
                                "description": product.Description,
                                "amount": amount,
                                "price": product.Price,
                                "total": total_price,
                            }
                            products_details_for_email.append(product_details)

                        except Products.DoesNotExist:
                            print(f"Product with id {id_product} does not exist.")

            # Obtener el email del usuario para enviar el correo electrónico

            user_email = serializer.data.get("UserEmail", None)
            address1 = serializer.data.get("Address1", None)
            name = serializer.data.get("Name", None)
            totalPriceOrder = serializer.data.get("TotalPrice", None)

            first_deposit = totalPriceOrder / 2
            second_deposit = totalPriceOrder / 2

            id_product_order = 100000 + id_product
            identity_document = serializer.data.get("IdentityDocument", None)
            creation_date_str = serializer.data.get("creationDate", None)
            # Ajustar la fecha restando 5 horas y formatearla como DD/MM/YYYY
            if creation_date_str:
                creation_date = datetime.fromisoformat(
                    creation_date_str.replace("Z", "")
                )
                creation_date -= timedelta(hours=5)
                creation_date_formatted = creation_date.strftime("%d/%m/%Y %H:%M")
            else:
                creation_date_formatted = None
            # Enviar correo electrónico con los detalles del pedido
            if user_email and products_details_for_email:
                context = {
                    "name": name,
                    "products": products_details_for_email,
                    "order_id": id_product_order + totalPriceOrder,
                    "address1": address1,
                    "identity_document": identity_document,
                    "creationDate": creation_date_formatted,
                    "id_product_order": id_product_order,
                    "totalPriceOrder": totalPriceOrder,
                    "first_deposit": first_deposit,
                    "second_deposit": second_deposit,
                }

                html_message = render_to_string("order_item_email.html", context)
                subject = "INKACUEROS PERÚ, El pedido ha sido registrado con éxito"
                email = EmailMessage(
                    subject, html_message, "your_email@example.com", [user_email]
                )
                email.content_subtype = "html"
                email.send()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
