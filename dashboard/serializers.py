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


class CreateProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('name', 'skills', 'description','end_date', 'category', 'creator')

    def validate(self, data):
        attrs = super(CreateProjectSerializer, self).validate(data)  # calling default validation
        # skills must be child of category skill
        for x in data['skills']:
            parent_skill = x
            while True:
                print(parent_skill)
                parent_skill = Skill.objects.get(name=parent_skill)
                print(parent_skill.skill_id)
                if parent_skill.skill_id is None:
                    if Skill.objects.get(name = parent_skill) != data['category']:
                        print(attrs['category'])
                        raise serializers.ValidationError('مهارت انتخاب شده فرزند زمینه نیست')
                    else :
                        break
                else:
                    parent_skill = Skill.objects.get(code= parent_skill.skill_id).name   
        return data

    def validate_category(self, value):
        # category must be a parent skill
        if Skill.objects.get(name=value).skill_id is not None:
            raise serializers.ValidationError('زمینه باید یک مهارت پدر باشد.')
        return value

    def validate_skills(self, value):
        # number of skills must be between 3 to 10
        if not (len(value) >= 3 and len(value) <= 10):
            raise serializers.ValidationError('تعداد مهارت ها باید بین ۳ تا ۱۰ باشد.')
        return value