from django.test import TestCase
from model_bakery import baker
from accounts.models import Project, UserProject, User
from datetime import datetime,timedelta


class TestSaveProject(TestCase):
    def setUp(self):
        self.project = baker.make(Project)
        self.user = baker.make(User)
        self.user_project = baker.make(UserProject, user=self.user, project=self.project)

    def test_change_status_to_start(self):
        self.project.status='STARTED'
        self.project.save()
        self.assertLessEqual(datetime.now()-self.project.start_date,timedelta(minutes=1))

    def test_change_status_to_ended(self):
        self.project.status = 'ENDED'
        self.project.save()
        self.assertLessEqual(datetime.now()-self.project.end_date,timedelta(minutes=1))
        self.assertEqual(UserProject.objects.filter(project=self.project,status='PENDING').count(), 0)

    def test_change_status_to_deleted(self):
        self.project.status = 'DELETED'
        self.project.save()
        self.assertEqual(UserProject.objects.filter(project=self.project,status='PENDING').count(), 0)

class TestUpdatePermissionProject(TestCase):

    def setUp(self):
        self.project = baker.make(Project,status='WAITING')
        baker.make(UserProject,project=self.project,status='PENDING')
        self.user = baker.make(User)
        self.user_project = baker.make(UserProject,user=self.user,project=self.project)

    def test_permission_for_not_user_project(self):
        other_user = baker.make(User)
        self.assertFalse(self.project.object_update_permission(other_user))

    def test_permission_for_ended(self):
        self.project.status = 'ENDED'
        self.project.save()
        self.assertFalse(self.project.object_update_permission(self.user))

    def test_permission_for_deleted(self):
        self.project.status = 'DELETED'
        self.project.save()
        self.assertFalse(self.project.object_update_permission(self.user))

    def test_permission_for_admin(self):
        self.user_project.status='ADMIN'
        self.user_project.save()
        self.assertTrue(self.project.object_update_permission(self.user))

    def test_permission_for_creator(self):
        self.user_project.status='CREATOR'
        self.user_project.save()
        self.assertTrue(self.project.object_update_permission(self.user))

    def test_permission_for_other(self):
        self.user_project.status='DELETED'
        self.user_project.save()
        self.assertFalse(self.project.object_update_permission(self.user))

class TestDestroyPermissionProject(TestCase):

    def setUp(self):
        self.project = baker.make(Project,status='WAITING')
        self.user = baker.make(User)
        self.user_project = baker.make(UserProject,user=self.user,project=self.project,status='CREATOR')

    def test_permission_for_not_user_project(self):
        other_user = baker.make(User)
        self.assertFalse(self.project.object_destroy_permission(other_user))

    def test_permission_for_creator(self):
        self.assertTrue(self.project.object_destroy_permission(self.user))

    def test_permission_for_other(self):
        other_user = baker.make(User)
        baker.make(UserProject, user=other_user, project=self.project, status='ACCEPTED')
        self.assertFalse(self.project.object_update_permission(other_user))


