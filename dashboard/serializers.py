from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from accounts.models import *
from django.utils.translation import gettext_lazy as _


class ProjectBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name', 'description',)


class Status:
    def __init__(self, code, label):
        self.code = code
        self.label = label


class StatusSerializer(serializers.Serializer):
    code = serializers.CharField()
    label = serializers.CharField()


class UserProjectSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='project.name')
    description = serializers.ReadOnlyField(source='project.description')
    role = serializers.CharField(source='get_role_display')
    status = SerializerMethodField()

    class Meta:
        model = UserProject
        exclude = ('id', 'user', 'admin')

    """Do not display role when category is REQUEST"""
    def __init__(self, *args, **kwargs):
        query_params = kwargs['context']['request'].query_params
        if (len(query_params) != 0) and query_params['category'] == 'REQUEST':
            del self.fields['role']
        super().__init__(*args, **kwargs)

    def get_status(self, instance):
        query_params = self.context['request'].query_params
        if len(query_params) != 0:
            if query_params['category'] == 'PROJECT':
                return StatusSerializer(
                    Status(code=instance.project.status, label=instance.project.get_status_display)).data
            else:
                return StatusSerializer(
                    Status(code=instance.status, label=instance.get_status_display)).data
        else:
            return StatusSerializer(
                Status(code=instance.project.status, label=instance.project.get_status_display)).data


class CreateProjectSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.get_full_name')

    class Meta:
        model = Project
        fields = ('name', 'skills', 'description', 'end_date', 'category', 'creator')

    def validate(self, data):
        data = super(CreateProjectSerializer, self).validate(data)  # calling default validation
        # skills must be child of category skill
        for skill in data['skills']:
            parent_skill = skill
            while parent_skill.skill:
                parent_skill = parent_skill.skill
            if parent_skill != data['category']:
                raise serializers.ValidationError(
                    {'skills': [_('The {} skill is not in the {} category').format(skill.name, data['category'].name)]})
        return data

    def validate_category(self, value):
        # category must be a parent skill
        if value.skill:
            raise serializers.ValidationError(_('The category should be a father skill.'))
        return value

    def validate_skills(self, value):
        # number of skills must be between 3 to 10
        if not (len(value) >= 3 and len(value) <= 10):
            raise serializers.ValidationError(_('The number of skills must be between {} and {}').format(3, 10))
        return value
