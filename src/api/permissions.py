from rest_framework import permissions


class ProjectOwnerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        # Give permissions for GET requests
        if request.method == "GET":
            return True
        # If the user is not authenticated block the access
        if request.user.is_authenticated is False:
            return False
        # Return true if the edited object belong to the user
        return obj.project in request.user.projects.all()
