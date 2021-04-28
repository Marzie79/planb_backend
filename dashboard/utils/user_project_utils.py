from django.db.models import Q

from accounts.models import Project


class ProjectTeamUtils:
    @staticmethod
    def is_higher_level_teammate(higer_user, lower_user):
        projects = Project.objects.filter(
            Q(userproject__user=higer_user) & (Q(userproject__status='CREATOR') | Q(userproject__status='ADMIN')))
        is_member = projects.filter(
            Q(userproject__user=lower_user) & ~Q(userproject__status='DELETED'))
        if is_member.exists():
            return True
        return False

    @staticmethod
    def is_higher_level_or_self(higer_user, lower_user):
        if ((higer_user == lower_user or ProjectTeamUtils.is_higher_level_teammate(higer_user, lower_user))):
            return True
        return False
