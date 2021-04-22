from django.contrib.auth.models import User, Group
from api.models import (
    Project,
    Sequence,
    Shot,
    Frame,
    Asset,
    Task
)
from rest_framework import serializers

########################################
## Serializers creates the available fileds in the REST api
########################################

# Set the user serializers
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


# Set the user serializers
class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

# Set the project serializers
class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

# Set the sequence serializers
class SequenceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sequence
        fields = '__all__'

# Set the shot serializers
class ShotSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Shot
        fields = '__all__'

# Set the frame serializers
class FrameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Frame
        fields = '__all__'

# Set the asset serializers
class AssetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Asset
        fields = '__all__'

# Set the task serializers
class TaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
