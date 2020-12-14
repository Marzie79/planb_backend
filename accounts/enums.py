from enum import Enum
from planB_backend.settings import local


class Email(Enum):
    EMAIL_ADDRESS = local.EMAIL_HOST_USER
    PASSWORD = local.EMAIL_HOST_PASSWORD


class FrontURL(Enum):
    FORGET_PASSWORD = '/user/forget-password/verify?code='
    SIGNUP = '/user/signup/verify?code='
    ROOT = 'http://127.0.0.1:3000/'
