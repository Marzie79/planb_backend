from enum import Enum


class Email(Enum):
    EMAIL_ADDRESS = 'planbkhu@gmail.com'
    PASSWORD = '1234planB'


class FrontURL(Enum):
    FORGET_PASSWORD = '/users/forget-password/verify?code='
    SIGNUP = '/users/signup/verify?code='
