from rest_framework import status
from rest_framework.exceptions import APIException


class BadRequestError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'bad_request'


class ServerError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_code = 'server_error'


class FormValidationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'form_validation'
