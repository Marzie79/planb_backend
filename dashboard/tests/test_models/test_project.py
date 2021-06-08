from os import stat_result
from django.test import TestCase
from model_bakery import baker
from accounts.models import Project, UserProject, User, user_project
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
        self.assertFalse(self.project.object_destroy_permission(self.user))

    def test_permission_for_other(self):
        other_user = baker.make(User)
        baker.make(UserProject, user=self.user, project=self.project, status='ADMIN')
        self.assertFalse(self.project.object_update_permission(other_user))


class TestTeamProject(TestCase):
    def setUp(self):
        self.project = baker.make(Project)
        self.user = baker.make(User)
        self.user_project = baker.make(UserProject, user=self.user, project=self.project)

    def test_object_read_permission(self):
        other_user = baker.make(User)
        self.assertEqual(self.user_project.object_read_permission({'status' : 'PENDING'},self.user), False)
        self.assertEqual(self.user_project.object_read_permission({'status' : 'PENDING'},other_user), False)
        self.assertEqual(self.user_project.object_read_permission({'status' : 'DECLINED'},self.user), True)

    def test_object_update_permission(self):
        project = baker.make(Project, status = "ENDED")
        other_user = baker.make(User)
        user_project = baker.make(UserProject, user=self.user, project=project)
        self.assertEqual(user_project.object_update_permission(self.user, other_user, 'ACCEPTED'), False)
        
        new_project = baker.make(Project, status = 'STARTED')
        new_user_project = baker.make(UserProject, user=self.user, project=new_project, status='ADMIN')
        self.assertEqual(new_user_project.object_update_permission(self.user, self.user, 'DELETED'), True)
        self.assertEqual(new_user_project.object_update_permission(self.user, other_user, 'DECLINED'), True)
        self.assertEqual(new_user_project.object_update_permission(other_user, self.user, 'ACCEPTED'), False)

    def test_object_create_permission(self):
        project = baker.make(Project, status = "ENDED")
        other_user = baker.make(User)
        user_project = baker.make(UserProject, user=self.user, project=project)
        self.assertEqual(user_project.object_create_permission(self.user, other_user, 'PENDING'), False)

        new_project = baker.make(Project, status = 'STARTED')
        new_user_project = baker.make(UserProject, user=self.user, project=new_project, status='ADMIN')
        self.assertEqual(new_user_project.object_create_permission(self.user, self.user, 'PENDING'), True)
        self.assertEqual(new_user_project.object_create_permission(self.user, self.user, 'ACCEPTED'), True)
        self.assertEqual(new_user_project.object_create_permission(other_user, self.user, 'ACCEPTED'), False)
