from rest_framework import permissions


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
       return obj.owner == request.user


class ReadOnly(permissions.BasePermission):

    def has_permisison(self, request, view):
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return obj.is_public
