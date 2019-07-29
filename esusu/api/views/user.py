from ..models import User
from ..serializers import BaseUserSerializer, UserRegistrationSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class UserView(APIView):
    """
    List all users, or create a new snippet.
    """
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = BaseUserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        model_serializer = BaseUserSerializer(data=request.data)
        model_serializer.is_valid(raise_exception=True)
        data = model_serializer.create_user()
        return Response(BaseUserSerializer(data).data, status=status.HTTP_201_CREATED)
