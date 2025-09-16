from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny

from apps.restaurants.serializers import RestaurantSerializer, MenuSerializer


class RestaurantListView(ListAPIView):
    """
    View to list all restaurants.
    """
    permission_classes = [AllowAny]

    serializer_class = RestaurantSerializer
    queryset = RestaurantSerializer.Meta.model.objects.all()


class RestaurantDetailView(RetrieveAPIView):
    """
    View to retrieve a single restaurant by its ID.
    """
    permission_classes = [AllowAny]

    serializer_class = RestaurantSerializer
    queryset = RestaurantSerializer.Meta.model.objects.all()
    lookup_field = 'id'


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


