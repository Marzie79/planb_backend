from rest_framework import serializers
from accounts.models import *


class ProjectBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name', 'description',)


class UserProjectSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display', read_only=True)
    name = serializers.ReadOnlyField(source='project.name')
    description = serializers.ReadOnlyField(source='project.description')
    role =  serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = UserProject
        exclude = ('id', 'user','admin' )