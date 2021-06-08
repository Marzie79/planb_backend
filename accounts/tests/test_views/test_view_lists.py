from django.urls import reverse

from core.tests.openapi_tester import BaseAPITestCase


class ListViewTest(BaseAPITestCase):

    def test_profile_endpoints(self):
        self.assertResponse(self.client.get(reverse('list_city')))
        self.assertResponse(self.client.get(reverse('list_province')))
        self.assertResponse(self.client.get(reverse('list_university')))
        self.assertResponse(self.client.get('list_skill'))
