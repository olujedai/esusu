from django.urls import path
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase

from ..models import Society
from ..views import SocietyView


class SocietyTests(APITestCase):
    def setUp(self):
        self.valid_payload = {
            'name': 'test@Society.com',
            'description': 'Test',
            'maximum_capacity': 'User',
            'periodic_amount': 'testpassword',
            'is_searchable': True,
        }
        self.view = SocietyView.as_view()
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
