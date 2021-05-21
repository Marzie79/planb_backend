from openapi_tester.schema_tester import SchemaTester
from rest_framework.test import APITestCase
from rest_framework.response import Response

schema_tester = SchemaTester()


class BaseAPITestCase(APITestCase):
    """ Base test class for api views including schema validation """

    @staticmethod
    def assertResponse(response: Response, **kwargs) -> None:
        """ helper to run validate_response and pass kwargs to it """