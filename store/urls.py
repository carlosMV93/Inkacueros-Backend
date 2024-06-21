from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

from .views import (
    TypeViewSet,
    BrandViewSet,
    ProductsViewSet,
    ProductsOrdersViewSet,
    OrdersViewSet,
    OrderItemViewSet,
    OrderItemDetailView,
    OrderItemListView,
    ProductsListViewSet,
    SendPasswordEmailView,
    ChangePasswordView,
    OrderItemCreateView,
)


router = DefaultRouter()
router.register(r"type", TypeViewSet, basename="type")
router.register(r"brand", BrandViewSet, basename="brand")
router.register(r"products", ProductsViewSet, basename="products")
router.register(r"productsorder", ProductsOrdersViewSet, basename="productsorder")
router.register(r"orders", OrdersViewSet, basename="orders")
router.register(r"orderitem", OrderItemViewSet, basename="orderitem")


urlpatterns = [
    path("", include(router.urls)),
    path("validate_user", views.user_login, name="validate_user"),
    path("create_user", views.create_user, name="create_user"),
    path("change-password", ChangePasswordView.as_view(), name="change_password"),
    path("order-items/", OrderItemListView.as_view(), name="order-item-list"),
    path("product-items/", ProductsListViewSet.as_view(), name="product-item-list"),
    path(
        "send-password-email/",
        SendPasswordEmailView.as_view(),
        name="send-password-email",
    ),
    path(
        "order-item/<int:id>/",
        OrderItemDetailView.as_view(),
        name="order-item-detail",
    ),
    path(
        "order-item-create/",
        OrderItemCreateView.as_view(),
        name="order-item-detail",
    ),
]
