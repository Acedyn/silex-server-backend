from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers
from api.models import Project, Sequence, Shot, Frame, Asset, Task

########################################
## Serializers creates the available fileds in the REST api
########################################

# Set the user serializers
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "url",
            "username",
            "email",
            "groups",
            "is_superuser",
            "first_name",
            "last_name",
            "password",
            "projects",
        ]
        read_only_fields = ("projects", "is_superuser", "date_joined")


# Set the user serializers
class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]


# Set the project serializers
class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"
        read_only_fields = ("deleted_at", "updated_at", "created_at")


# Set the sequence serializers
class SequenceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sequence
        fields = "__all__"
        read_only_fields = ("deleted_at", "updated_at", "created_at")


# Set the shot serializers
class ShotSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Shot
        fields = "__all__"
        read_only_fields = ("deleted_at", "updated_at", "created_at")


# Set the frame serializers
class FrameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Frame
        fields = "__all__"
        read_only_fields = ("deleted_at", "updated_at", "created_at")


# Set the asset serializers
class AssetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Asset
        fields = "__all__"
        read_only_fields = ("deleted_at", "updated_at", "created_at")


# Set the task serializers
class TaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = ("deleted_at", "updated_at", "created_at")
