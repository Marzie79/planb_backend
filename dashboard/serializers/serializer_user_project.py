
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from accounts.models import *

from core.fields import CustomHyperlinkedRelatedField

class StatusSerializer(serializers.Serializer):
    code = serializers.CharField(source='status')
    label = serializers.CharField(source='get_status_display')
    # def __init__(self, instance):
    #     # Don't pass the 'fields' arg up to the superclass
    #     if instance is None:
    #         super(StatusSerializer, self).__init__(None)
    #     else:
    #         super(StatusSerializer, self).__init__(instance)


class ProjectStatusSerializer(serializers.ModelSerializer):
    role = SerializerMethodField()
    status = SerializerMethodField()

    class Meta:
        model = Project
        fields = ('name', 'status', 'role')

    def get_status(self, instance):
        return StatusSerializer(instance).data

    def get_role(self, instance):
        try:
            role = UserProject.objects.get(Q(user=self.context['request'].user) & Q(project=instance))
        except:
            role = None
        return StatusSerializer(role).data


class UserProjectSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='project.name')
    description = serializers.ReadOnlyField(source='project.description')
    role = serializers.CharField(source='get_role_display')
    status = SerializerMethodField()
    url = CustomHyperlinkedRelatedField(
        **{'source': 'project', 'lookup_field': 'slug', 'read_only': 'True', 'view_name': 'project-detail'})

    class Meta:
        model = UserProject
        fields = ('name', 'description', 'role', 'status', 'url',)
        # exclude = ('id', 'user',)

    """Do not display role when category is REQUEST"""

    def __init__(self, *args, **kwargs):
        query_params = kwargs['context']['request'].query_params
        if ('category' in query_params) and query_params['category'] == 'REQUEST':
            del self.fields['role']
        super().__init__(*args, **kwargs)

    def get_status(self, instance):
        query_params = self.context['request'].query_params
        if ('category' in query_params) and query_params['category'] != 'PROJECT':
            return StatusSerializer(instance).data
        return StatusSerializer(instance.project).data
