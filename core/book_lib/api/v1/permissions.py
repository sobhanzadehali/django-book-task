from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsVerified(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_verified

    def has_object_permission(self, request, view, obj):
        return request.user.is_verified
