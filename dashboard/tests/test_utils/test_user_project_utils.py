from django.test import TestCase
from model_bakery import baker

from accounts.models import Project, User, UserProject
from dashboard.utils.user_project_utils import ProjectTeamUtils


class TestIsHigherLevelTeammate(TestCase):
    def setUp(self):
        self.first_project = baker.make(Project)
        self.second_project = baker.make(Project)
        self.lower_user = baker.make(User)
        self.higer_user = baker.make(User)

    def test_is_higher_teammate(self):
        higher_user_project = UserProject.objects.create(project=self.first_project, user=self.higer_user,
                                                         status='ADMIN')
        lower_user = UserProject.objects.create(project=self.first_project, user=self.lower_user,
                                                status='ACCEPTED')
        self.assertTrue(ProjectTeamUtils.is_higher_level_teammate(self.higer_user, self.lower_user))
        higher_user_project.status = 'CREATOR'
        higher_user_project.save()
        self.assertTrue(ProjectTeamUtils.is_higher_level_teammate(self.higer_user, self.lower_user))

    def test_is_not_higher_teammate(self):
        not_higher_user_project = UserProject.objects.create(project=self.first_project, user=self.higer_user,
                                                             status='ACCEPTED')
        UserProject.objects.create(project=self.first_project, user=self.lower_user,
                                   status='ACCEPTED')
        self.assertFalse(ProjectTeamUtils.is_higher_level_teammate(self.higer_user, self.lower_user))
        not_higher_user_project.status = 'PENDING'
        not_higher_user_project.save()
        self.assertFalse(ProjectTeamUtils.is_higher_level_teammate(self.higer_user, self.lower_user))

    def test_is_deleted_teammate(self):
        UserProject.objects.create(project=self.first_project, user=self.higer_user,
                                   status='ADMIN')
        UserProject.objects.create(project=self.first_project, user=self.lower_user,
                                   status='DELETED')
        self.assertFalse(ProjectTeamUtils.is_higher_level_teammate(self.higer_user, self.lower_user))


    def test_is_not_teammate(self):
        UserProject.objects.create(project=self.first_project, user=self.lower_user,
                                   status='ACCEPTED')
        self.assertFalse(ProjectTeamUtils.is_higher_level_teammate(self.higer_user, self.lower_user))
        UserProject.objects.create(project=self.second_project, user=self.higer_user,
                                   status='ADMIN')
        self.assertFalse(ProjectTeamUtils.is_higher_level_teammate(self.higer_user, self.lower_user))
