from .serializers import *
from accounts.views.view_profile import ProfileUser


class UserSkill(ProfileUser):

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserSkillSerializer
        elif self.action == 'partial_update':
            return UpdateSkillSerializer
