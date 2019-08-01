from django.urls import path
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import User
from api.views import UserView
from rest_framework.test import APIRequestFactory

class UserTests(APITestCase):
    def setUp(self):
        self.valid_payload = {
            'email': 'test@user.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword',
            'confirm_password': 'testpassword',
        }
        self.password_mismatch_payload = {
            'email': 'password@user.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword',
            'confirm_password': 'nomatch',
        }
        self.existing_user_payload = {
            'email': 'existing@user.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword',
        }
        self.existing_user = User.objects.create_user(**self.existing_user_payload)
        self.view = UserView.as_view()
        self.url = path('user/', self.view)
        self.factory = APIRequestFactory()


    def test_valid_signup(self):
        """
        Ensure we can signup a new user with valid credentials.
        """
        request = self.factory.post(self.url, data=self.valid_payload, format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(User.objects.filter(email=self.valid_payload['email']).first())


    def test_user_cannot_signup_twice(self):
        """
        Ensure a user cannot signup twice.
        """
        self.existing_user_payload['confirm_password'] = self.existing_user_payload['password']
        request = self.factory.post(self.url, data=self.existing_user_payload, format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['email'][0], 'This email address already exists.')

    def test_password_match(self):
        """
        Ensure password and confirm_password fields are equal.
        """
        request = self.factory.post(self.url, data=self.password_mismatch_payload, format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0], 'Passwords don\'t match.')
