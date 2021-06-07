from django.test import TestCase
from model_bakery import baker
from accounts.models import User, Project, UserProject


class TestTeamProject(TestCase):
    def setUp(self):
        self.project = baker.make(Project)
        self.user = baker.make(User)
        self.user_project = baker.make(UserProject, user=self.user, project=self.project)

    def test_has_object_read_permission(self):
        self.user_project.status = 'CREATOR'
        self.user_project.save()
        self.assertTrue(self.user_project.object_read_permission({'status' : 'PENDING'},self.user))
