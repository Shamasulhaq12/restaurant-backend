from django.contrib import admin

from .models import (
    Restaurant,
    RestaurantImage,
    Menu,
    MenuItem,
    MenuItemIngredient,
    Category,
    Orders,
    OrderItem,
    Review,
)


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone_number', 'email')
    search_fields = ('name', 'address', 'phone_number', 'email')
    ordering = ('name',)

@admin.register(RestaurantImage)
class RestaurantImageAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'is_primary')
    search_fields = ('restaurant__name',)
    list_filter = ('is_primary',)
    ordering = ('restaurant',)

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant')
    search_fields = ('name', 'restaurant__name')
    list_filter = ('restaurant',)
    ordering = ('restaurant', 'name')

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'menu', 'price')
    list_filter = ('menu',)
    ordering = ('menu', 'name')

@admin.register(MenuItemIngredient)
class MenuItemIngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'menu_item', 'quantity')
    search_fields = ('name', 'menu_item__name')
    list_filter = ('menu_item',)
    ordering = ('menu_item', 'name')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'order_type', 'order_status', 'created_at')
    search_fields = ('user__first_name', 'user__last_name', 'billing_email', 'billing_phone')
    list_filter = ('order_type', 'order_status', 'created_at')
    ordering = ('-created_at',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('menu_item', 'quantity', 'price')
    search_fields = ('menu_item__name',)
    ordering = ('menu_item',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'order', 'rate', 'created_at')
    search_fields = ('user__first_name', 'user__last_name', 'order__user__user_type')
    list_filter = ('rate', 'created_at')
    ordering = ('-created_at',)
