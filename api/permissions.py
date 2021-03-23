from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsActiveUserPermission(BasePermission):

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                and request.user
                and request.user.is_authenticated
                and request.user.is_active)


class IsOwner(IsActiveUserPermission):

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsStaff(IsActiveUserPermission):

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff
