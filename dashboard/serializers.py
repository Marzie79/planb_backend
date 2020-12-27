from rest_framework import serializers
from accounts.models import *
from django.utils.translation import gettext_lazy as _


class ProjectBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name', 'description',)


class UserProjectSerializer(serializers.ModelSerializer):
    status_UserProject = serializers.CharField(source='status')
    status_Project = serializers.ReadOnlyField(source='project.status')
    name = serializers.ReadOnlyField(source='project.name')
    description = serializers.ReadOnlyField(source='project.description')
    role = serializers.CharField(source='get_role_display')

    class Meta:
        model = UserProject
        exclude = ('id', 'user', 'admin', 'status')

    """Do not display status_UserProject when category is PROJECT or NULL"""
    def __init__(self, *args, **kwargs):
        try:
            if kwargs['context']['request'].query_params['category'] == 'PROJECT':
                del self.fields['status_UserProject']
        except:
            del self.fields['status_UserProject']
        super().__init__(*args, **kwargs)


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
            raise serializers.ValidationError(_('The background should be a father skill.'))
            raise serializers.ValidationError(_('The category should be a father skill.'))
        return value

    def validate_skills(self, value):
        # number of skills must be between 3 to 10
        if not (len(value) >= 3 and len(value) <= 10):
            raise serializers.ValidationError(_('The number of skills must be between {} and {}').format(3, 10))
        return value
