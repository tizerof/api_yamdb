from rest_framework.permissions import SAFE_METHODS, BasePermission

from authentication.models import User


class IsActiveUserPermission(BasePermission):

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user
                and request.user.is_authenticated
                and request.user.is_active)


class IsOwner(IsActiveUserPermission):

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsAdmin(IsActiveUserPermission):

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.user.role == User.Roles.ADMIN


class IsModerator(IsActiveUserPermission):
    def has_object_permission(self, request, view, obj):
        return (request.user.is_staff
                or request.user.role == User.Roles.MODERATOR)
