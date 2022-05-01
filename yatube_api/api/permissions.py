from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class AlllButAuthorReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS or obj.author == request.user:
            return True
        return False
