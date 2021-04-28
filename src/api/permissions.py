from rest_framework import permissions
from api.utils import get_instance_from_url
from api.models import Project


class ProjectOwnerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Restict access only for POST requests
        if request.method != "POST":
            return True
        # If the user is not authenticated block the access
        if request.user.is_authenticated is False:
            return False

        parent_url = request.data[view.parents_chain[0]]
        parent = get_instance_from_url(
            parent_url, view.parent_model_class, view.parents_chain[0]
        )
        # If the direct parent if the entity is already the project
        if isinstance(parent, Project):
            # Check if the project belong to the user
            return parent in request.user.projects.all() or parent.owner == request.user

        # Check if the parent's project belong to the user
        return (
            parent.project in request.user.projects.all()
            or parent.project.owner == request.user
        )

    def has_object_permission(self, request, view, obj):
        # Give permissions for GET requests
        if request.method == "GET":
            return True
        # If the user is not authenticated block the access
        if request.user.is_authenticated is False:
            return False
        # Return true if the edited object belong to the user
        return (
            obj.project in request.user.projects.all()
            or obj.project.owner == request.user
        )
