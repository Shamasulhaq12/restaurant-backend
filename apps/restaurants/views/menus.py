from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.restaurants.models import Restaurant
from apps.restaurants.serializers import (
    RestaurantSerializer,
    MenuSerializer,
    RestaurantImageSerializer
)
from apps.userprofile.permissions import IsSuperAdmin


class RestaurantViewSet(ModelViewSet):
    """
    A ViewSet to list, create, retrieve, update, and delete restaurants.
    """
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        # only admins can create, update, delete
        return [IsSuperAdmin()]

    @action(detail=True, methods=['post'], permission_classes=[IsSuperAdmin])
    def upload_image(self, request, pk=None):
        """Custom endpoint for uploading a restaurant image"""
        restaurant = get_object_or_404(Restaurant, pk=pk)
        serializer = RestaurantImageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(restaurant=restaurant)
        return Response(serializer.data)

    @action(detail=True, methods=['put'], permission_classes=[IsSuperAdmin])
    def update_image(self, request, pk=None):
        """Custom endpoint for uploading a restaurant image"""
        restaurant = get_object_or_404(Restaurant, pk=pk)
        serializer = RestaurantImageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(restaurant=restaurant)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsSuperAdmin], url_path="lite")
    def lite(self, request):
        """
        Lite version of restaurant list:
        - Only returns id + name
        - Search by `?search=`
        - Ordered alphabetically
        - Max 10 results when searching
        """
        qs = Restaurant.objects.only("id", "name").order_by("name")

        search_query = request.query_params.get("search")
        if search_query:
            qs = qs.filter(Q(name__icontains=search_query))[:10]
        else:
            qs = qs[:10]  # default also capped at 10

        data = [{"id": r.id, "name": r.name} for r in qs]
        return Response(data)

class MenuListView(ListAPIView):
    """
    View to list all menus for a specific restaurant.
    """
    permission_classes = [AllowAny]
    serializer_class = MenuSerializer

    def get_queryset(self):
        """
        Returns the queryset of menus filtered by the restaurant ID provided in the URL.
        """
        restaurant_id = self.kwargs.get('restaurant_id')
        return MenuSerializer.Meta.model.objects.filter(restaurant_id=restaurant_id)

class MenuDetailView(RetrieveAPIView):
    """
    View to retrieve a single menu by its ID.
    """
    permission_classes = [AllowAny]
    serializer_class = MenuSerializer
    queryset = MenuSerializer.Meta.model.objects.all()
    lookup_field = 'id'

class MenuItemListView(ListAPIView):
    """
    View to list all menu items for a specific menu.
    """
    permission_classes = [AllowAny]
    serializer_class = MenuSerializer

    def get_queryset(self):
        """
        Returns the queryset of menu items filtered by the menu ID provided in the URL.
        """
        menu_id = self.kwargs.get('menu_id')
        return MenuSerializer.Meta.model.objects.filter(id=menu_id).prefetch_related('menu_items')

class MenuItemDetailView(RetrieveAPIView):
    """
    View to retrieve a single menu item by its ID.
    """
    permission_classes = [AllowAny]
    serializer_class = MenuSerializer
    queryset = MenuSerializer.Meta.model.objects.all()
    lookup_field = 'id'
