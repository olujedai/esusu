from django.urls import path
from rest_framework import status
from rest_framework.test import (APIRequestFactory, APITestCase,
                                 force_authenticate)

from api.models import Society
from api.views import SearchSocietiesView, SocietyContributions, SocietyView

from .utils import (add_user_to_society, create_fake_society,
                    delete_all_societies, get_auth_token, get_fake_user,
                    get_test_user)


class SocietyTests(APITestCase):
    def setUp(self):
        self.valid_payload = {
            'name': 'Team Comfam',
            'description': 'Esusu society for staff of Team Confam',
            'maximum_capacity': 10,
            'periodic_amount': 100000,
            'is_searchable': True,
        }
        self.user = get_test_user()
        self.token = get_auth_token()
        self.society_view = SocietyView.as_view()
        self.society_url = path('society/', self.society_view)

        self.search_society_view = SearchSocietiesView.as_view()
        self.search_society_url = path('society/search/', self.search_society_view)

        self.society_contributions_view = SocietyContributions.as_view()
        self.society_contributions_url = path('society/contributions/', self.society_contributions_view, name='society-contribution')

        self.factory = APIRequestFactory()

    def test_user_can_create_a_society(self):
        """
        Ensure a new user can setup a new esusu society.
        """
        self.assertEqual(self.user.is_society_admin, False)

        request = self.factory.post(self.society_url, data=self.valid_payload, HTTP_AUTHORIZATION=f'Bearer {self.token}', format='json')
        force_authenticate(request, user=self.user)
        response = self.society_view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        society = Society.objects.filter(name=self.valid_payload['name']).first()
        self.assertIsNotNone(society)
        self.assertEqual(society.admin, self.user)
        self.user.refresh_from_db()
        self.assertEqual(self.user.is_society_admin, True)
        self.user.society = None
        self.user.is_society_admin = False
        self.user.save()
        society.delete()

    
    def test_user_cannot_create_multiple_societies(self):
        society = create_fake_society()
        creator = society.admin
        self.assertEqual(creator.is_society_admin, True)

        request = self.factory.post(self.society_url, data=self.valid_payload, HTTP_AUTHORIZATION=f'Bearer {get_auth_token(creator)}', format='json')
        force_authenticate(request, user=creator)
        response = self.society_view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_search_for_public_societies(self):
        delete_all_societies()
        create_fake_society(searchable=True)
        searchable_society = Society.objects.filter(is_searchable=True).first()
        
        creator = searchable_society.admin
        request = self.factory.get(self.search_society_url, {'name': searchable_society.name}, HTTP_AUTHORIZATION=f'Bearer {get_auth_token(creator)}')
        force_authenticate(request, user=creator)
        response = self.search_society_view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_cannot_search_for_private_societies(self):
        delete_all_societies()
        create_fake_society(searchable=False)
        unsearchable_society = Society.objects.filter(is_searchable=False).first()
        
        fake_user = get_fake_user()
        request = self.factory.get(self.search_society_url, {'name': unsearchable_society.name}, HTTP_AUTHORIZATION=f'Bearer {get_auth_token(fake_user)}')
        force_authenticate(request, user=fake_user)
        response = self.search_society_view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
    
    def test_can_view_society_users_and_contribution(self):
        society = create_fake_society()
        user = add_user_to_society(society)

        admin_user = society.admin

        request = self.factory.get(self.society_contributions_url, {'': ''}, HTTP_AUTHORIZATION=f'Bearer {get_auth_token(admin_user)}')
        force_authenticate(request, user=admin_user)
        response = self.society_contributions_view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user_request = self.factory.get(self.society_contributions_url, {'': ''}, HTTP_AUTHORIZATION=f'Bearer {get_auth_token(user)}')
        force_authenticate(user_request, user=user)
        response = self.society_contributions_view(user_request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
