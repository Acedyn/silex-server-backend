from django.contrib.auth.models import User, Group
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
