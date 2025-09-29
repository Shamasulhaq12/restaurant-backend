from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSuperAdmin(BasePermission):
    """
    Allows access only to super_admin users.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.user_type == "super_admin"
        )

class IsSuperAdminOrReadOnly(BasePermission):
    """
    Allow only super_admins to create/update/delete.
    Others can only view (GET, HEAD, OPTIONS).
    """

    def has_permission(self, request, view):
        # Safe methods are always allowed (GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return True

        # For write methods, check if super_admin
        return (
            request.user.is_authenticated
            and request.user.user_type == "super_admin"
        )


class IsSuperAdminOrRestaurantOwner(BasePermission):
    """
    SuperAdmin: Full access
    RestaurantOwner: Only manage waiters in their own restaurant
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if hasattr(request.user, "restaurant_owner"):
            return obj.restaurant.owner == request.user
        return False

    def has_permission(self, request, view):
        return request.user.is_authenticated