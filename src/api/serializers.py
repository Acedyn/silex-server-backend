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
            "password",
            "projects",
        ]
        read_only_fields = ("username", "projects", "is_superuser", "date_joined")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password")
        groups = []
        if "groups" in validated_data:
            groups = validated_data.pop("groups")
        validated_data["username"] = validated_data["email"].split("@")[0]
        user = get_user_model()(**validated_data)
        user.set_password(password)
        user.save()
        user.groups.set(groups)
        user.save()
        return user


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
        read_only_fields = ("deleted_at", "updated_at", "created_at", "owner", "name")


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
