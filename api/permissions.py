from rest_framework.permissions import SAFE_METHODS, BasePermission

from authentication.models import User


class IsActiveUserPermission(BasePermission):

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated
                and request.user.is_active)


class IsOwner(IsActiveUserPermission):

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or obj.author == request.user)


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return (request.user.is_authenticated
                and request.user.is_active
                and (request.user.is_staff
                     or request.user.role == User.Roles.ADMIN))

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return (request.user.is_staff
                or request.user.role == User.Roles.ADMIN)


class IsAdminOrReadOnlyCGT(IsActiveUserPermission):

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_superuser
                )


class IsModerator(IsActiveUserPermission):
    def has_object_permission(self, request, view, obj):
        return (request.user.is_staff
                or request.user.role == User.Roles.MODERATOR)
