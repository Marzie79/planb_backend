from enum import Enum
from planB_backend.settings import local


class Email(Enum):
    EMAIL_ADDRESS = local.EMAIL_HOST_USER
    PASSWORD = local.EMAIL_HOST_PASSWORD


class FrontURL(Enum):
    FORGET_PASSWORD = '/users/forget-password/verify?code='
    SIGNUP = '/users/signup/verify?code='
    ROOT = 'http://1127.0.0.1:3000/'
