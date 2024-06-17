from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

from .views import (
    TypeViewSet,
    BrandViewSet,
    ProductsViewSet,
    OrdersViewSet,
    OrderItemViewSet,
)


router = DefaultRouter()
router.register(r"type", TypeViewSet, basename="type")
router.register(r"brand", BrandViewSet, basename="brand")
router.register(r"products", ProductsViewSet, basename="products")
router.register(r"orders", OrdersViewSet, basename="orders")
router.register(r"orderitem", OrderItemViewSet, basename="orderitem")


urlpatterns = [
    path("", include(router.urls)),
    path("validate_user", views.user_login, name="validate_user"),
    path("create_user", views.create_user, name="create_user"),
]
