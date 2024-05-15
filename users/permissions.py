from rest_framework import permissions


class IsVerified(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.verified


class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.position == 'manager')


class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.position == 'owner')


class IsOwnerOrManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.position == 'owner' or request.user.position == 'manager')


class IsSelf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user
