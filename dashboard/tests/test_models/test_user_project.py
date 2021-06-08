from django.test import TestCase
from model_bakery import baker
from accounts.models import User, Project, UserProject


class TestTeamProject(TestCase):
    def setUp(self):
        self.project = baker.make(Project)
        self.user = baker.make(User)
        self.user_project = baker.make(UserProject, user=self.user, project=self.project)

    def test_object_read_permission(self):
        other_user = baker.make(User)
        self.assertEqual(self.user_project.object_read_permission({'status': 'PENDING'}, self.user), False)
        self.assertEqual(self.user_project.object_read_permission({'status': 'PENDING'}, other_user), False)
        self.assertEqual(self.user_project.object_read_permission({'status': 'DECLINED'}, self.user), True)

    def test_object_update_permission(self):
        project = baker.make(Project, status="ENDED")
        other_user = baker.make(User)
        user_project = baker.make(UserProject, user=self.user, project=project)
        self.assertEqual(user_project.object_update_permission(self.user, other_user, 'ACCEPTED'), False)

        new_project = baker.make(Project, status='STARTED')
        new_user_project = baker.make(UserProject, user=self.user, project=new_project, status='ADMIN')
        self.assertEqual(new_user_project.object_update_permission(self.user, self.user, 'DELETED'), True)
        self.assertEqual(new_user_project.object_update_permission(self.user, other_user, 'DECLINED'), True)
        self.assertEqual(new_user_project.object_update_permission(other_user, self.user, 'ACCEPTED'), False)

    def test_object_create_permission(self):
        project = baker.make(Project, status="ENDED")
        other_user = baker.make(User)
        user_project = baker.make(UserProject, user=self.user, project=project)
        self.assertEqual(user_project.object_create_permission(self.user, other_user, 'PENDING'), False)
        new_project = baker.make(Project, status='STARTED')
        new_user_project = baker.make(UserProject, user=self.user, project=new_project, status='ADMIN')
        self.assertEqual(new_user_project.object_create_permission(self.user, self.user, 'PENDING'), True)
        self.assertEqual(new_user_project.object_create_permission(self.user, self.user, 'ACCEPTED'), True)
        self.assertEqual(new_user_project.object_create_permission(other_user, self.user, 'ACCEPTED'), False)
