from rest_framework.permissions import SAFE_METHODS, BasePermission

from authentication.models import User


class IsOwner(BasePermission):

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated
                and request.user.is_active)

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


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return (request.user.is_authenticated
                and request.user.is_active
                and (request.user.is_staff
                     or request.user.role == User.Roles.ADMIN))

    def has_object_permission(self, request, view, obj):
        return (request.user.is_staff
                or request.user.role == User.Roles.MODERATOR)
