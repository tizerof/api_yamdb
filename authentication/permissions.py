from rest_framework.permissions import SAFE_METHODS, BasePermission

from authentication.models import User


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        else:
            if request.user.is_staff or request.user.role == User.Roles.ADMIN:
                return True


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False

        if request.user.is_staff or request.user.role == 'admin':
            return True
