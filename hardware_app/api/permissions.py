from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsStoreManagerOrReadOnly(BasePermission):
    """
    Store Managers and superusers can modify products.
    Other authenticated users can only view products.
    """

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        if user.is_superuser:
            return True

        if request.method in SAFE_METHODS:
            return True

        return user.groups.filter(name="Store Manager").exists()