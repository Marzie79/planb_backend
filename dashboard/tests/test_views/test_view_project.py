from django.urls import reverse
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import Project, User, Skill, UserProject
from core.tests.openapi_tester import BaseAPITestCase


class ProjectViewGetTest(BaseAPITestCase):
    def setUp(self):
        self.project = baker.make(Project)
        self.client = APIClient()
        self.list_url = reverse('project-list')
        self.detail_url = reverse('project-detail', kwargs={'slug': self.project.slug})
        self.status_url = reverse('project-get_status', kwargs={'slug': self.project.slug})

    def test_project_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_project_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_project_status(self):
        response = self.client.get(self.status_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_project_endpoints(self):
        self.assertResponse(self.client.get(self.list_url))
        self.assertResponse(self.client.get(self.detail_url))


class ProjectViewCreateTest(BaseAPITestCase):
    def setUp(self):
        self.client = APIClient()
        self.list_url = reverse('project-list')
        self.user = baker.make(User)
        self.client.force_authenticate(self.user)
        self.category = baker.make(Skill)
        self.skill = baker.make(Skill, skill=self.category)

    def test_project_create(self):
        self.client.post(self.list_url, {
            "amount": 10,
            "name": "string",
            "description": "string",
            "endDate": "2030-06-07T18:02:40.542Z",
            "skills": [
                self.skill.id
            ],
            "category": self.category.id,
        })
        self.assertEqual(self.user, UserProject.objects.last().user)


class ProjectViewUpdateTest(BaseAPITestCase):
    def setUp(self):
        self.client = APIClient()
        user = baker.make(User)
        self.client.force_authenticate(user)
        self.project = baker.make(Project,status='WAITING')
        self.detail_url = reverse('project-detail', kwargs={'slug': self.project.slug})
        baker.make(UserProject,user=user,project=self.project,status='CREATOR')

    def test_project_delete(self):
       response = self.client.patch(self.detail_url, {
            "status": "DELETED",
        })
       self.assertEqual(response.status_code, status.HTTP_200_OK)
       self.assertEqual(Project.objects.all().count(),0)

    def test_project_not_delete(self):
        response = self.client.patch(self.detail_url, {
            "status": "STARTED",
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Project.objects.all().count(),1)


