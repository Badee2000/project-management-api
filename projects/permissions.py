from rest_framework import permissions


class IsOwnerOrManagerOrBelongsTo(permissions.BasePermission):
    def has_permission(self, request, view):
        project = view.get_object()
        return (request.user == project.manager or
                request.user in project.manager.projects.all() or
                request.user == project.company.owner)
