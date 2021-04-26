from urllib.parse import urlparse
from django.contrib.auth.models import User, Group
from django.db.models import Model
from django.utils.text import slugify
from django.urls import resolve
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework import permissions, viewsets, status, serializers
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from api.models import Project, Sequence, Shot, Frame, Asset, Task
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
    serializer_class = serializers.HyperlinkedModelSerializer
    parent_model_class = Model
    parent_model_name = "undefined"
    parents_chain = ()

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
        # Get the parent to inherit metadata
        if self.parent_model_name in updated_data:
            # Get the project from the url
            parent_path = urlparse(updated_data[self.parent_model_name]).path
            try:
                parent_match = resolve(parent_path)
                parent_queryset = self.parent_model_class.objects.all()
                parent = parent_queryset.get(id=parent_match.kwargs["pk"])

                # Override the fields that where not set in the input request
                if "framerate" not in updated_data:
                    updated_data["framerate"] = parent.framerate
                if "width" not in updated_data:
                    updated_data["width"] = parent.width
                if "height" not in updated_data:
                    updated_data["height"] = parent.height

            except Exception as ex:
                # Just print the exeption as a warning, the error will be thrown by the serializer
                print(
                    f"WARNING: {type(ex)} : \
                    Could not get parent field values for request : {request.data}"
                )

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
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]


# Inteface to edit/view groups
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]


# Inteface to edit/view projects
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    # Override the method called when creating an project (POST) to auto fill the name field
    def create(self, request, *args, **kwargs):
        # Make a copy of the data object because it's immutable
        updated_data = request.data.copy()
        # Set the name according to the given label
        if "label" in updated_data:
            updated_data["name"] = slugify(updated_data["label"])

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
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    parent_model_class = Project
    parent_model_name = "project"
    parents_chain = ("project",)


# Inteface to edit/view shots
class ShotViewSet(ParentedEntityViewSet):
    queryset = Shot.objects.all()
    serializer_class = ShotSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    parent_model_class = Sequence
    parent_model_name = "sequence"
    parents_chain = ("sequence", "project")

    # Override the method called when creating an project (POST) to auto fill the parents fields
    def create(self, request, *args, **kwargs):
        # Make a copy of the data object because it's immutable
        updated_data = request.data.copy()
        # If no sequence where given, don't do anything
        # The error will be raised by the serializer
        if "sequence" not in updated_data:
            return super().create(request=request, *args, **kwargs)

        # Get the sequence from the url
        sequence_path = urlparse(updated_data["sequence"]).path
        try:
            sequence_match = resolve(sequence_path)
            sequence_queryset = Sequence.objects.all()
            sequence = sequence_queryset.get(id=sequence_match.kwargs["pk"])

            # Set the parent field from the given sequence
            project_url = (
                str(reverse(viewname="project-list", request=request))
                + str(sequence.project.id)
                + "/"
            )
            updated_data["project"] = project_url

        except Exception as ex:
            # Just print the exeption as a warning, the error will be thrown by the serializer
            print(
                f"WARNING: {type(ex)} : \
                Could not find parent from url for request : {request.data}"
            )

        return super().create(request=request, data=updated_data, *args, **kwargs)


# Inteface to edit/view frames
class FrameViewSet(ParentedEntityViewSet):
    queryset = Frame.objects.all()
    serializer_class = FrameSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    parent_model_class = Shot
    parent_model_name = "shot"
    parents_chain = ("shot", "sequence", "project")

    # Override the method called when creating an project (POST) to auto fill the parents fields
    def create(self, request, *args, **kwargs):
        # Make a copy of the data object because it's immutable
        updated_data = request.data.copy()
        # If no shot where given, don't do anything
        # The error will be raised by the serializer
        if "shot" not in updated_data:
            return super().create(request=request, *args, **kwargs)

        # Get the shot from the url
        shot_path = urlparse(updated_data["shot"]).path
        try:
            shot_match = resolve(shot_path)
            shot_queryset = Shot.objects.all()
            shot = shot_queryset.get(id=shot_match.kwargs["pk"])

            # Set the parent field from the given shot
            sequence_url = (
                str(reverse(viewname="sequence-list", request=request))
                + str(shot.sequence.id)
                + "/"
            )
            updated_data["sequence"] = sequence_url
            project_url = (
                str(reverse(viewname="project-list", request=request))
                + str(shot.sequence.project.id)
                + "/"
            )
            updated_data["project"] = project_url

        except Exception as ex:
            # Just print the exeption as a warning, the error will be thrown by the serializer
            print(
                f"WARNING: {type(ex)} : \
                Could not find parent from url for request : {request.data}"
            )

        return super().create(request=request, data=updated_data, *args, **kwargs)


# Inteface to edit/view assets
class AssetViewSet(ParentedEntityViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    parent_model_class = Project
    parent_model_name = "project"
    parents_chain = ("project",)


# Inteface to edit/view tasks
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]