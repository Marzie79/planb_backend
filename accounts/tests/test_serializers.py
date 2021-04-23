from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from accounts.models import Skill, User
from accounts.serializers.serializer_profile import UserSkillSerializer
import json


# class ProfileSerializerTest(APITestCase):
#     def setUp(self):
#         self.skill = baker.make(Skill, _quantity=3)
#         self.user = baker.make(User, skills=self.skill)
#         self.client = APIClient()
#
#     def test_UserSkillSerializer(self):
#         payload = UserSkillSerializer(self.user).data
#         response = self.client.patch('/user/skills/', json.dumps(payload), format='json')
#         # self.assertTrue(payload.isvalid())
#         self.assertEqual(response.status_code, status.HTTP_200_OK)