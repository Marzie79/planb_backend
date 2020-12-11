from rest_framework import viewsets
from .serializers import *


class UserSkill(viewsets.ReadOnlyModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = UserSkillSerializer

    def get_queryset(self):
        return self.request.user.skills


class ChildSkill(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = ChildSkillSerializer

    def get_queryset(self):
        skill_id = self.kwargs['current_skill_id']
        return Skill.objects.filter(skill_id=skill_id)
