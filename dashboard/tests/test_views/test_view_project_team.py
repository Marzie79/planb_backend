import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient, RequestsClient
from model_bakery import baker
from accounts.models import *
from core.tests.openapi_tester import BaseAPITestCase
from dashboard.views.view_project_team import get_update_text


class ProjectTeamViewTest(BaseAPITestCase):

    def setUp(self):
        self.user = baker.make(User)
        self.project = baker.make(Project)
        self.user_project = baker.make(UserProject, user=self.user, project=self.project, status='ADMIN')
        self.client = APIClient()
        self.url_list = reverse('project_members-list', kwargs={'slug_slug': self.project.slug})

    def test_list(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_request_member(self):
        new_user = baker.make(User)
        self.client.force_authenticate(new_user)
        response = self.client.post(self.url_list, {
            "status": "PENDING",
            "user": new_user.id,
            "project": self.project.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # def test_category_request(self):
    #     data = {"category": "REQUEST"}
    #     self.client.force_authenticate(user=self.user)
    #     response = self.client.get(self.url, data)
    #     user_projects = json.loads(response.content)
    #     for item in user_projects:
    #         if item["status"]["code"] not in ["DECLINED", "PENDING"]:
    #             assert (status.HTTP_400_BAD_REQUEST_)
    #     assert response.status_code == status.HTTP_200_OK

    def test_partial_update(self):
        self.client.force_authenticate(self.user)
        new_user = baker.make(User)
        baker.make(UserProject, user=new_user, project=self.project, status='ACCEPTED')
        url_detail = reverse('project_members-detail', kwargs={'slug_slug': self.project.slug,'username':new_user.username})
        response = self.client.patch(url_detail, {
            "status": "DELETED",
            "user": new_user.id,
            "project": self.project.id
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_project_endpoints(self):
        self.assertResponse(self.client.get(self.url_list))




class ProjectTeamTextTest(BaseAPITestCase):
    def setUp(self) :
        self.name='test'


    def test_accepted(self):
        status='ACCEPTED'
        get_update_text(self.name,status)

    def test_deleted(self):
        status = 'DELETED'
        get_update_text(self.name, status)

    def test_declined(self):
        status = 'DECLINED'
        get_update_text(self.name, status)

    def test_admin(self):
        status = 'ADMIN'
        get_update_text(self.name, status)





