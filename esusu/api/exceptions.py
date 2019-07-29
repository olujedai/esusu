from rest_framework.exceptions import APIException
from django.utils.encoding import force_text
from rest_framework import status


class CustomException(APIException):

    def __init__(self, detail, status_code):
        self.detail = force_text(detail)
        self.status_code = status_code