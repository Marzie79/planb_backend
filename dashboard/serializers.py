from rest_framework import serializers
from accounts.models import *


class ProjectBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name', 'description', )


class UserProjectSerializer(serializers.ModelSerializer):
    project = ProjectBriefSerializer()

    class Meta:
        model = UserProject
        exclude = ('user', )
