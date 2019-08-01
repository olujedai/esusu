from django.urls import path
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase

from ..models import Society
from ..views import SocietyView
from .utils import get_auth_token, get_test_user
from rest_framework.test import force_authenticate


class SocietyTests(APITestCase):
    def setUp(self):
        self.valid_payload = {
            'name': 'Team Comfam',
            'description': 'Esusu group for staff of Team Confam',
            'maximum_capacity': 10,
            'periodic_amount': 100000,
            'is_searchable': True,
        }

        self.user = get_test_user()
        self.token = get_auth_token()
        self.view = SocietyView.as_view()
        self.url = path('society/', self.view)
        self.factory = APIRequestFactory()

    def test_society_creation(self):
        """
        Ensure a new user can setup a new esusu group.
        """
        self.assertEqual(self.user.is_society_admin, False)

        request = self.factory.post(self.url, data=self.valid_payload, HTTP_AUTHORIZATION=f'Bearer {self.token}', format='json')
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        society = Society.objects.filter(name=self.valid_payload['name']).first()
        self.assertIsNotNone(society)
        self.assertEqual(society.admin, self.user)
        self.user.refresh_from_db()
        self.assertEqual(self.user.is_society_admin, True)

