from rest_framework import permissions


class IsOwnerOrManagerOrBelongsTo(permissions.BasePermission):
    def has_permission(self, request, view):
        task = view.get_object()
        return (request.user == task.project.manager or
                request.user in task.project.manager.projects.all() or
                request.user == task.assigned_to or
                request.user == task.project.company.owner)
