from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models import Model
from django.utils.text import slugify
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions, viewsets, status, serializers
from api.utils import (
    request_inherit_fields,
    get_instance_from_url,
)
from api.models import Project, Sequence, Shot, Frame, Asset, Task, User
from api.permissions import (
    ProjectOwnerPermission,
    IsAuthenticatedOrReadCreate,
)
from api.serializers import (
    UserSerializer,
    GroupSerializer,
    ProjectSerializer,
    SequenceSerializer,
    ShotSerializer,
    FrameSerializer,
    AssetSerializer,
    TaskSerializer,
)

########################################
## Utility
########################################


# Abstract class to implement the inheritance of parent fields
class ParentedEntityViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ProjectOwnerPermission]
    serializer_class = serializers.HyperlinkedModelSerializer
    parent_model_class = Model
    parents_chain = ("undefined",)

    # Override the method called when creating an entity (POST) to auto fill the metadata fields
    def create(self, request, *args, **kwargs):
        # Take the data from the request only if no data parameters where given
        # This allow reusability of this function since request is immutable and can't be copied
        if "data" in kwargs:
            updated_data = kwargs["data"]
            kwargs.pop("data")
        else:
            # Make a copy of the data object because it's immutable
            updated_data = request.data.copy()
        # Inherit the data from the parents using the parent chain
        updated_data = request_inherit_fields(
            updated_data, request, self.parents_chain, self.parent_model_class
        )

        # Set the user foreign key for created_by and updated_by
        if request.user.is_authenticated and isinstance(request.user, User):
            owner_serializer = UserSerializer(
                instance=request.user, context={"request": request}
            )
            updated_data["created_by"] = owner_serializer["url"].value
            updated_data["updated_by"] = owner_serializer["url"].value

        # Set the state to active
        updated_data["state"] = "active"

        # Create the serializer using the updated input data
        serializer = self.serializer_class(
            data=updated_data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    # Override the method called when getting an entity (GET) to add a resolved root path
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        # Make a copy of the data object because it's immutable
        updated_data = serializer.data.copy()
        path = updated_data["root"]
        # Loop over all the parents and build the output path
        for parent in self.parents_chain:
            path = str(getattr(instance, parent).root) + path

        updated_data["path"] = path
        return Response(updated_data)

    # Override the method called when getting multiple entities (GET) to add a resolved root path
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            # Make a copy of the data object because it's immutable
            updated_data = serializer.data.copy()
            for data_index in range(len(updated_data)):
                path = updated_data[data_index]["root"]
                # Not sure using _args is the best solution here
                instance = serializer.child._args[0][data_index]
                # Loop over all the parents and build the output path
                for parent in self.parents_chain:
                    path = str(getattr(instance, parent).root) + path

                updated_data[data_index]["path"] = path

            return self.get_paginated_response(updated_data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


########################################
## Views are the interface between the user and the backend
########################################


# Inteface to edit/view users
class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadCreate]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user_class = get_user_model()
        token = RefreshToken.for_user(
            get_instance_from_url(response.data["url"], user_class)
        )
        response.data["access"] = str(token.access_token)
        response.data["refresh"] = str(token)
        return response


# Inteface to edit/view groups
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


# Inteface to edit/view projects
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Override the method called when creating an project (POST) to auto fill the name field
    def create(self, request, *args, **kwargs):
        # Make a copy of the data object because it's immutable
        updated_data = request.data.copy()
        # Set the name according to the given label
        if "label" in updated_data:
            updated_data["name"] = slugify(updated_data["label"])
        # Set the user foreign key for created_by and updated_by
        if request.user.is_authenticated and isinstance(request.user, User):
            owner_serializer = UserSerializer(
                instance=request.user, context={"request": request}
            )
            updated_data["created_by"] = owner_serializer["url"].value
            updated_data["updated_by"] = owner_serializer["url"].value

        # Set the state to active
        updated_data["state"] = "active"

        # Create the serializer using the updated input data
        serializer = ProjectSerializer(data=updated_data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    # Override the method called when getting a project (GET) to add a resolved root path
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        # Make a copy of the data object because it's immutable
        updated_data = serializer.data.copy()
        # We just pass the same value as root
        # We do that to have consistant response so the "path" entry is always there
        updated_data["path"] = updated_data["root"]
        return Response(updated_data)

    # Override the method called when getting multiple projects (GET) to add a resolved root path
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            # Make a copy of the data object because it's immutable
            updated_data = serializer.data.copy()
            for single_data in updated_data:
                # We just pass the same value as root
                # We do that to have consistant response so the "path" entry is always there
                single_data["path"] = single_data["root"]
            return self.get_paginated_response(updated_data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# Inteface to edit/view sequence
class SequenceViewSet(ParentedEntityViewSet):
    queryset = Sequence.objects.all()
    serializer_class = SequenceSerializer
    parent_model_class = Project
    parents_chain = ("project",)


# Inteface to edit/view shots
class ShotViewSet(ParentedEntityViewSet):
    queryset = Shot.objects.all()
    serializer_class = ShotSerializer
    parent_model_class = Sequence
    parents_chain = ("sequence", "project")


# Inteface to edit/view frames
class FrameViewSet(ParentedEntityViewSet):
    queryset = Frame.objects.all()
    serializer_class = FrameSerializer
    parent_model_class = Shot
    parents_chain = ("shot", "sequence", "project")


# Inteface to edit/view assets
class AssetViewSet(ParentedEntityViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    parent_model_class = Project
    parents_chain = ("project",)


# Inteface to edit/view tasks
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
