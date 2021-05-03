from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from api.utils import get_instance_from_url
from api.models import Project


class ProjectOwnerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # If the user has permissions to create any project
        if request.user.has_perm("api.add_any_entity") and request.method == "POST":
            return True
        # Restict access only for POST requests
        if request.method != "POST":
            return True
        # If the user is not authenticated block the access
        if request.user.is_authenticated is False:
            return False
        # If the request is empty it means its just a request poke the server
        if request.data == {}:
            return True
        # Test if the data provided the parent
        try:
            parent_url = request.data[view.parents_chain[0]]
        except Exception as ex:
            # If the parent could not be resolved, raise an exception
            raise ValidationError(
                {f"{view.parents_chain[0]}": ["This field is required."]}
            ) from ex
        parent = get_instance_from_url(
            parent_url, view.parent_model_class, view.parents_chain[0]
        )
        # If the direct parent if the entity is already the project
        if isinstance(parent, Project):
            # Check if the project belong to the user
            return (
                parent in request.user.projects.all()
                or parent.created_by == request.user
            )

        # Check if the parent's project belong to the user
        return (
            parent.project in request.user.projects.all()
            or parent.project.created_by == request.user
        )

    def has_object_permission(self, request, view, obj):
        # If the user has permissions to edit any project
        if request.user.has_perm("api.change_any_entity") and request.method == "PATCH":
            return True
        # If the user has permissions to delete any project
        if (
            request.user.has_perm("api.delete_any_entity")
            and request.method == "DELETE"
        ):
            return True
        # Give permissions for GET requests
        if request.method == "GET":
            return True
        # If the user is not authenticated block the access
        if request.user.is_authenticated is False:
            return False
        # Return true if the edited object belong to the user
        return (
            obj.project in request.user.projects.all()
            or obj.project.created_by == request.user
        )


class IsAuthenticatedOrReadCreate(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow only safe metods or creation for unauthentificated users
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.method == "POST"
            or request.user
            and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        # Allow only save methods
        return bool(request.method in permissions.SAFE_METHODS)
