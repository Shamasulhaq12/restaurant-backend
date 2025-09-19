from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.restaurants.views import (
    MenuListView,
    MenuDetailView,
    MenuItemListView,
    MenuItemDetailView,
    RestaurantListView,
    RestaurantDetailView,
    TableViewSet,
    QRScanView,
    CreateCartAPIView,
    CartItemCreateAPIView,
    RetrieveCartAPIView,
    DeleteCartItemAPIView,
    UpdateCartItemAPIView,
    ReviewViewSet,
    OrderCheckoutAPIView, UserOrderHistoryAPIView, WaiterOrderListAPIView,
)
from apps.restaurants.views.ai import (
    RestaurantTopSuggestionsView,
    RestaurantMenuSuggestionsView
)


router = DefaultRouter()
router.register(r'tables', TableViewSet, basename='table')
router.register(r'reviews', ReviewViewSet, basename='reviews')

urlpatterns = [
    path('', include(router.urls)),

    # Existing resources
    path('restaurants/', RestaurantListView.as_view(), name='restaurant-list'),
    path('restaurants/<int:id>/', RestaurantDetailView.as_view(),
         name='restaurant-detail'),
    path('restaurants/<int:restaurant_id>/menus/', MenuListView.as_view(),
         name='menu-list'),
    path('restaurants/<int:restaurant_id>/menus/<int:id>/',
         MenuDetailView.as_view(), name='menu-detail'),
    path('menus/<int:menu_id>/menu-items/', MenuItemListView.as_view(),
         name='menu-item-list'),
    path('menus/<int:menu_id>/menu-items/<int:id>/',
         MenuItemDetailView.as_view(), name='menu-item-detail'),

    # QR code scanning endpoint
    path("tables/scan-qr/", QRScanView.as_view(), name="scan-qr"),

    # AI suggestions endpoints
    path('ai/restaurants/suggestions/top/', RestaurantTopSuggestionsView.as_view(),
         name='restaurant-suggestions-top'),
    path('ai/restaurants/<int:restaurant_id>/menus/suggestions/',
         RestaurantMenuSuggestionsView.as_view(), name='restaurant-menu-suggestions'),

    # Cart and CartItem endpoints
    path('cart/create-cart/', CreateCartAPIView.as_view(), name='create-cart'),
    path('cart/create-cart-item/', CartItemCreateAPIView.as_view(),
         name='create-cart-item'),
    path('cart/retrieve-cart/', RetrieveCartAPIView.as_view(), name='retrieve-cart'),
    path('cart/delete-cart-item/<int:pk>/', DeleteCartItemAPIView.as_view(),
         name='delete-cart-item'),
    path('cart/update-cart-item/<int:pk>/', UpdateCartItemAPIView.as_view(),
         name='update-cart-item'),

    path('orders/checkout-order/', OrderCheckoutAPIView.as_view(), name='checkout-order'),
    path('orders/', UserOrderHistoryAPIView.as_view(), name='user-order-history'),
    path('orders/waiter/', WaiterOrderListAPIView.as_view(), name='waiter-order-list')
]
