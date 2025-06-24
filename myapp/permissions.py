from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of a task to edit/delete it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
