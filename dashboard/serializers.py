from django.utils import timezone
from phonenumber_field.phonenumber import to_python
from rest_framework import serializers, status
from rest_framework.fields import SerializerMethodField
from accounts.models import *
from django.utils.translation import gettext_lazy as _

from core.fields import CustomHyperlinkedRelatedField, CustomHyperlinkedIdentityField


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
        if (len(query_params) != 0) and query_params['category'] == 'REQUEST':
            del self.fields['role']
        super().__init__(*args, **kwargs)

    def get_status(self, instance):
        query_params = self.context['request'].query_params
        if ('category' in query_params) and query_params['category'] != 'PROJECT':
            return StatusSerializer(instance).data
        return StatusSerializer(instance.project).data


class ProjectSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.get_full_name')
    category = serializers.ReadOnlyField(source='category.name')
    skills = serializers.StringRelatedField(many=True)
    url = CustomHyperlinkedIdentityField(**{'lookup_field': 'slug', 'view_name': 'project-detail', })
    creator_url = CustomHyperlinkedRelatedField(
        **{'source': 'creator', 'lookup_field': 'username', 'read_only': 'True', 'view_name': 'user-detail'})
    status = SerializerMethodField()

    class Meta:
        model = Project
        fields = ('amount', 'name', 'skills', 'description', 'end_date', 'category', 'creator', 'creator_url', 'url', 'status')

    def get_status(self, instance):
        return StatusSerializer(instance).data


class ProjectSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('amount', 'name', 'skills', 'description', 'end_date', 'category', 'status')

    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        if self.context['view'].action == 'create':
            fields['status'].read_only = True
        return fields

    def validate(self, data):
        data = super(ProjectSaveSerializer, self).validate(data)  # calling default validation
        # skills must be child of category skill
        incorrect_skill = ''
        for skill in data['skills']:
            parent_skill = skill
            while parent_skill.skill:
                parent_skill = parent_skill.skill
            if parent_skill != data['category']:
                incorrect_skill += skill.name + ','
        if incorrect_skill:
            raise serializers.ValidationError(
                {'skills': [
                    _('The {} skill is not in the {} category').format(incorrect_skill[:-1], data['category'].name)]})
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

    def validate_end_date(self, value):
        # category must be a parent skill
        if not value or value < timezone.now():
            raise serializers.ValidationError(_('The {} must be bigger than today').format(_("End_Date")))
        return value

    def validate_status(self, value):
        STATUS = {'WAITING': 0,
                  'STARTED': 1,
                  'ENDED': 2,
                  'DELETED': 3}
        previous_status = self.instance.status
        if STATUS[value] >= STATUS[previous_status]:
            return value
        raise serializers.ValidationError(
            _('You have not been allowed to change the project into {} status.').format(_(value.title())))


class ProjectTeamSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(source='user.avatar', required=False, )
    city = serializers.ReadOnlyField(source='user.city.name')
    description = serializers.ReadOnlyField(source='user.description')
    name = serializers.ReadOnlyField(source='user.__str__')
    province = serializers.ReadOnlyField(source='user.city.province.name')
    role = serializers.ReadOnlyField(source='get_role_display')
    username = serializers.ReadOnlyField(source='user.username')
    url = CustomHyperlinkedRelatedField(
        **{'source': 'user', 'lookup_field': 'username', 'read_only': 'True', 'view_name': 'user-detail'})

    class Meta:
        model = UserProject
        fields = (
            'name', 'city', 'role', 'province', 'description', 'avatar', 'status', 'username', 'user', 'project', 'url')
        # extra_kwargs = {
        #     'status': {'write_only': True},
        # }


# class PersonSerializer(serializers.ModelSerializer):
#     city = serializers.ReadOnlyField(source='city.name')
#     name = serializers.ReadOnlyField(source='__str__')
#     province = serializers.ReadOnlyField(source='city.province.name')
#     role = serializers.ReadOnlyField(source='get_role_display')
#
#     class Meta:
#         model = User
#         fields = ('name', 'city', 'role', 'province', 'description', 'avatar', 'username')


class BriefSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('code', 'name')


class UserInfoSerializer(serializers.ModelSerializer):
    phone_number = serializers.SerializerMethodField('check_phone_number_visibility')
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)
    city = serializers.ReadOnlyField(source='city.name')
    province = serializers.ReadOnlyField(source='city.province.name')
    url = CustomHyperlinkedIdentityField(
        **{'lookup_field': 'username', 'read_only': 'True', 'view_name': 'user-detail'})
    skills = BriefSkillSerializer(read_only=True, many=True)
    university = serializers.ReadOnlyField(source='university.name')

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'university', 'gender_display', 'phone_number', 'city', 'resume',
            'province', 'description',
            'avatar', 'url', 'email', 'skills')

    def check_phone_number_visibility(self, instance):
        request_user = self.context['request'].user
        if instance.phone_number and request_user.is_authenticated:
            if instance.username == request_user.username or Project.objects.filter(
                    userproject__user__in=(request_user.id, instance.id)).exists():
                return to_python(instance.phone_number).as_e164
        else:
            return None
