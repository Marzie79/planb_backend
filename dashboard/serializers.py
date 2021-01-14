from rest_framework import serializers, status
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

    def __init__(self, instance):
        # Don't pass the 'fields' arg up to the superclass
        if instance is None:
            super(StatusSerializer, self).__init__(None)
        else:
            super(StatusSerializer, self).__init__(Status(code=instance.status, label=instance.get_status_display))


class UserProjectSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.ReadOnlyField(source='project.name')
    description = serializers.ReadOnlyField(source='project.description')
    role = serializers.CharField(source='get_role_display')
    status = SerializerMethodField()


    class Meta:
        model = UserProject
        fields = ('name', 'description', 'role', 'status', 'url',)
        # exclude = ('id', 'user',)
        extra_kwargs = {
            'url': {'lookup_field':'slug','read_only':'True','view_name':'project-detail','source':'project'}
        }

    """Do not display role when category is REQUEST"""

    def __init__(self, *args, **kwargs):
        query_params = kwargs['context']['request'].query_params
        if (len(query_params) != 0) and query_params['category'] == 'REQUEST':
            del self.fields['role']
        super().__init__(*args, **kwargs)

    def get_status(self, instance):
        query_params = self.context['request'].query_params
        if len(query_params) != 0 and query_params['category'] != 'PROJECT':
            return StatusSerializer(instance).data
        return StatusSerializer(instance.project).data


class ProjectSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.get_full_name')
    status = serializers.SerializerMethodField(method_name='get_status')

    # url = serializers.HyperlinkedIdentityField(view_name='project-detail')

    class Meta:
        model = Project
        fields = ('amount','name', 'skills', 'description', 'end_date', 'category', 'creator', 'url', 'status')
        extra_kwargs = {
            'url': {'lookup_field': 'slug'},
        }

    def get_status(self, instance):
        user = self.context['request'].user
        try:
            userProject = UserProject.objects.get(user=user, project=instance)
            return StatusSerializer(userProject).data
        except:
            return None

    def validate(self, data):
        data = super(ProjectSerializer, self).validate(data)  # calling default validation
        # skills must be child of category skill
        incorrect_skill=''
        for skill in data['skills']:
            parent_skill = skill
            while parent_skill.skill:
                parent_skill = parent_skill.skill
            if parent_skill != data['category']:
                incorrect_skill += skill.name + ','
        if incorrect_skill:
            raise serializers.ValidationError(
                    {'skills': [_('The {} skill is not in the {} category').format(incorrect_skill[:-1], data['category'].name)]})
        return data

    def validate_category(self, value):
        # category must be a parent skill
        if not value or value.skill:
            raise serializers.ValidationError(_('The category should be a father skill.'))
        return value

    def validate_skills(self, value):
        # number of skills must be between 3 to 10
        if not (len(value) >= 3 and len(value) <= 10):
            raise serializers.ValidationError(_('The number of skills must be between {} and {}').format(3, 10))
        return value


class ProjectTeamSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(source='user.avatar')
    city = serializers.ReadOnlyField(source='user.city.name')
    description = serializers.ReadOnlyField(source='user.description')
    name = serializers.ReadOnlyField(source='user.__str__')
    province = serializers.ReadOnlyField(source='user.city.province.name')
    role = serializers.ReadOnlyField(source='get_role_display')
    username = serializers.CharField(source='user.username')

    class Meta:
        model = UserProject
        fields = ('id', 'name', 'city', 'role', 'province', 'description', 'avatar', 'status', 'username')
        extra_kwargs = {
            'status': {'write_only': True},
        }
