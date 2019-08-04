from django.utils.encoding import force_text
from rest_framework import status
from rest_framework.exceptions import APIException


class CustomException(APIException):

    def __init__(self, detail, status_code):
        self.detail = force_text(detail)
        self.status_code = status_code

class MaximumMembersReachedException(CustomException):
    pass

class TenureDeadlinePassedException(CustomException):
    pass

class MemberAlreadyInASocietyException(CustomException):
    pass

class SocietyGoneException(CustomException):
    pass
