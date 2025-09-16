from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from apps.restaurants.models import Cart, CartItem, MenuItem
from apps.restaurants.serializers import CartSerializer, CartItemSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status


class CreateCartAPIView(CreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        cart, _ = Cart.objects.get_or_create(user=request.user.profile)

        return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)

class RetrieveCartAPIView(APIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            cart, _= Cart.objects.get_or_create(user=request.user.profile)

            return Response(CartSerializer(cart).data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CartItemCreateAPIView(CreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            menu_item = request.data.get('menu_item')
            quantity = request.data.get('quantity')
            restaurant = request.data.get('restaurant')
            cart, _ = Cart.objects.get_or_create(user=request.user.profile)
            menu_item = get_object_or_404(MenuItem, id=menu_item)

            if not menu_item:
                return Response({"message": "This product is not available."},)
            return Response(CartItemSerializer(menu_item).data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UpdateCartItemAPIView(UpdateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        try:
            cart_item = self.get_object()
            quantity = request.data.get('quantity')
            menu_item = cart_item.menu_item
            if menu_item:
                cart = get_object_or_404(Cart, items=cart_item)
                cart.total_price -= cart_item.size.price * cart_item.quantity
                cart_item.quantity = quantity
                cart_item.save()
                cart.total_price += cart_item.size.price * quantity
                menu_item.save()
                cart.save()
                return Response(CartSerializer(cart).data)
            else:
                return Response({
                    "message": f"{menu_item.name} not available."
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class DeleteCartItemAPIView(DestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        try:
            cart_item = self.get_object()
            cart = get_object_or_404(Cart, items=cart_item)
            cart.total_price -= cart_item.size.price * cart_item.quantity
            cart.save()
            cart_item.menu_item.save()
            cart_item.delete()
            return Response(CartSerializer(cart).data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# class CartItemViewSet(ModelViewSet):
#     queryset = CartItem.objects.all()
#     serializer_class = CartItemSerializer
#
#     def perform_create(self, serializer):
#         # Custom logic on create
#         cart_item = serializer.save()
#         cart = cart_item.cart
#         cart.total_price = sum(item.price * item.quantity for item in cart.cart_items.all())
#         cart.save()
#
#     def perform_update(self, serializer):
#         cart_item = serializer.save()
#         cart = cart_item.cart
#         cart.total_price = sum(item.price * item.quantity for item in cart.cart_items.all())
#         cart.save()
#
#     def perform_destroy(self, instance):
#         cart = instance.cart
#         instance.delete()
#         cart.total_price = sum(item.price * item.quantity for item in cart.cart_items.all())
#         cart.save()
