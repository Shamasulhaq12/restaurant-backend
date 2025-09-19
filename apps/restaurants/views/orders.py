from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now

from apps.restaurants.models import Cart, Orders, OrderItem
from apps.restaurants.serializers import OrderDetailSerializer, OrderSerializer


class OrderCheckoutAPIView(APIView):
    """
    Convert the current user's cart into an order.
    Supports both dine-in and online orders.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_profile = request.user.profile

        try:
            cart = Cart.objects.get(user=user_profile)
        except Cart.DoesNotExist:
            return Response({"detail": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)

        if not cart.cart_items.exists():
            return Response({"detail": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

        order_type = request.data.get("order_type", "DINE_IN")

        # Base order data
        order_data = {
            "user": user_profile,
            "ordered_date": now(),
            "order_type": order_type,
            "ordered": True,
            "payment_status": "Pending",
            "total_price": cart.total_price,
        }

        # Dine-in fields
        if order_type == "DINE_IN":
            order_data["table_id"] = request.data.get("table")
            order_data["waiter_id"] = request.data.get("waiter")

        # Online fields
        else:
            order_data["billing_first_name"] = request.data.get("billing_first_name")
            order_data["billing_last_name"] = request.data.get("billing_last_name")
            order_data["billing_email"] = request.data.get("billing_email")
            order_data["billing_phone"] = request.data.get("billing_phone")
            order_data["billing_address"] = request.data.get("billing_address")
            order_data["shipping_address"] = request.data.get("shipping_address")

        # Create order
        order = Orders.objects.create(**order_data)

        # Copy cart items → order items
        for cart_item in cart.cart_items.all():
            order_item = OrderItem.objects.create(
                menu_item=cart_item.menu_item,
                quantity=cart_item.quantity,
                comments=cart_item.comments,
                price=cart_item.price,
            )
            order.items.add(order_item)

        order.save()

        # Empty cart
        cart.cart_items.all().delete()
        cart.update_total_price()

        return Response(OrderDetailSerializer(order).data, status=status.HTTP_201_CREATED)

class WaiterOrderListAPIView(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Orders.objects.filter(waiter=self.request.user.profile).order_by("-created_at")

class UserOrderHistoryAPIView(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Orders.objects.filter(user=self.request.user.profile).order_by("-created_at")
