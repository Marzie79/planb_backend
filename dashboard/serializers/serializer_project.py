from django.utils import timezone
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from accounts.models import *
from django.utils.translation import gettext_lazy as _

from accounts.serializers import SkillBriefSerializer
from core.fields import CustomHyperlinkedRelatedField, CustomHyperlinkedIdentityField
from core.helpers.main_helper import make_notification_and_message
from core.helpers.make_message import make_message
from core.helpers.make_notification import make_notification
from dashboard.serializers.serializer_user_project import StatusSerializer


class ProjectSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.get_full_name')
    category = serializers.ReadOnlyField(source='category.name')
    category_id = serializers.ReadOnlyField(source='category.id')
    skills = SkillBriefSerializer(many=True)
    url = CustomHyperlinkedIdentityField(**{'lookup_field': 'slug', 'view_name': 'project-detail', })
    creator_url = CustomHyperlinkedRelatedField(
        **{'source': 'creator', 'lookup_field': 'username', 'read_only': 'True', 'view_name': 'user-detail'})
    status = SerializerMethodField()

    class Meta:
        model = Project
        fields = (
            'amount', 'name', 'skills', 'description', 'end_date', 'category', 'creator', 'creator_url', 'url',
            'status', 'category_id')

    def get_status(self, instance):
        return StatusSerializer(instance).data


class ProjectSaveSerializer(serializers.ModelSerializer):
    url = CustomHyperlinkedIdentityField(**{'lookup_field': 'slug', 'view_name': 'project-detail', })

    class Meta:
        model = Project
        fields = ('amount', 'name', 'skills', 'description', 'end_date', 'category', 'status', 'url')

    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        if self.context['view'].action == 'create':
            fields['status'].read_only = True
        return fields

    def validate(self, data):
        data = super(ProjectSaveSerializer, self).validate(data)  # calling default validation
        # skills must be child of category skill
        if 'skills' in data and 'category' in data:
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
                        _('The {} skill is not in the {} category').format(incorrect_skill[:-1],
                                                                           data['category'].name)]})
        return data

    def validate_category(self, value):
        # category must be a parent skill
        if not value or value.skill:
            raise serializers.ValidationError(_('The category should be a father skill.'))
        return value

    def validate_skills(self, value):
        # number of skills must be between 3 to 10
        if not len(value) <= 10:
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
            if STATUS[value] > STATUS[previous_status]:
                status = _('Started')
                if value == "ENDED":
                    status = _("Ended")
                elif value == "DELETED":
                    status = _('Deleted')
                text = _('The project {} status changed to {}').format(self.instance.name, status)
                make_notification_and_message(text, self.instance, statuses=["PENDING", "ACCEPTED", "ADMIN"])
                # recievers = UserProject.objects.filter(project=self.instance).filter(status__in=["PENDING", "ACCEPTED", "ADMIN"])
                # recievers_user = []
                # for item in recievers:
                #     recievers_user.append(item.user)
                # recievers_token = list(NotificationToken.objects.filter(user__in=recievers_user).values_list('token', flat=True))
                # make_message(text=text, receiver= recievers, project= self.instance)
                # make_notification(recievers_token, self.instance.name, text)

            return value
        raise serializers.ValidationError(
            _('You have not been allowed to change the project into {} status.').format(_(value.title())))
