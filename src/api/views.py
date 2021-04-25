from urllib.parse import urlparse
from django.contrib.auth.models import User, Group
from django.utils.text import slugify
from django.urls import resolve, Resolver404
from rest_framework.response import Response
from rest_framework import permissions, viewsets, status
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

    # Override the method called when creating an project to auto fill the name field
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


# Inteface to edit/view sequence
class SequenceViewSet(viewsets.ModelViewSet):
    queryset = Sequence.objects.all()
    serializer_class = SequenceSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    # Override the method called when creating an project to auto fill the metadata fields
    def create(self, request, *args, **kwargs):
        # Make a copy of the data object because it's immutable
        updated_data = request.data.copy()
        # Get the parent to inherit metadata
        if "project" in updated_data:
            # Get the project from the url
            parent_project_path = urlparse(updated_data["project"]).path
            try:
                parent_project_match = resolve(parent_project_path)
                parent_queryset = Project.objects.all()
                parent_project = parent_queryset.get(
                    id=parent_project_match.kwargs["pk"]
                )

                # Override the fields that where not set in the input request
                if "framerate" not in updated_data:
                    updated_data["framerate"] = parent_project.framerate
                if "width" not in updated_data:
                    updated_data["width"] = parent_project.width
                if "height" not in updated_data:
                    updated_data["height"] = parent_project.height

            except Exception as ex:
                # Just print the exeption as a warning, the error will be thrown by the serializer
                print(
                    f"WARNING: {type(ex)} : Could not get parent field values for request : {request.data}"
                )

        # Create the serializer using the updated input data
        serializer = SequenceSerializer(data=updated_data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


# Inteface to edit/view shots
class ShotViewSet(viewsets.ModelViewSet):
    queryset = Shot.objects.all()
    serializer_class = ShotSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]


# Inteface to edit/view frames
class FrameViewSet(viewsets.ModelViewSet):
    queryset = Frame.objects.all()
    serializer_class = FrameSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]


# Inteface to edit/view assets
class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]


# Inteface to edit/view tasks
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]
