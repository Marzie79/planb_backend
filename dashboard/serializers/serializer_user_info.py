from django.db.models import Q
from phonenumber_field.phonenumber import to_python
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from accounts.models import User, Project, Skill
from core.fields import CustomHyperlinkedIdentityField
from dashboard.utils.user_project_utils import ProjectTeamUtils


class BriefSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('code', 'name')


class UserBriefInfoSerializer(serializers.ModelSerializer):
    city = serializers.ReadOnlyField(source='city.name')
    province = serializers.ReadOnlyField(source='city.province.name')
    url = CustomHyperlinkedIdentityField(
        **{'lookup_field': 'username', 'read_only': 'True', 'view_name': 'user-detail'})

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'description','avatar', 'url', 'city','province')


class UserInfoSerializer(UserBriefInfoSerializer):
    phone_number = serializers.SerializerMethodField('check_phone_number_visibility')
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)

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
        if request_user.is_authenticated and ProjectTeamUtils.is_higher_level_or_self(request_user,instance):
            return to_python(instance.phone_number).as_e164
        return _('You have not been allowed to see {}').format(_('Phone_Number'))
