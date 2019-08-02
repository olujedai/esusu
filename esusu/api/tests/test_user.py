from django.urls import path
from rest_framework import status
from rest_framework.test import (APIRequestFactory, APITestCase,
                                 force_authenticate)

from api.exceptions import (MaximumMembersReachedException,
                            MemberAlreadyInASocietyException,
                            SocietyGoneException,
                            TenureDeadlinePassedException)
from api.models import User
from api.serializers import UserInvitationSerializer
from api.views import InviteUserToSocietyView, UserView

from .utils import (create_fake_society,create_tenure, empty_society,
                    fill_up_society, get_auth_token, get_deadline,
                    get_fake_user)


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
        self.user_view = UserView.as_view()
        self.user_url = path('user/', self.user_view)

        self.invite_sender_view = InviteUserToSocietyView.as_view()
        self.invite_sender_url = 'invite/society/<int:pk>/'
        self.factory = APIRequestFactory()

    def test_valid_signup(self):
        """
        Ensure we can signup a new user with valid credentials.
        """
        request = self.factory.post(self.user_url, data=self.valid_payload, format='json')
        response = self.user_view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(User.objects.filter(email=self.valid_payload['email']).first())

    def test_user_cannot_signup_twice(self):
        """
        Ensure a user cannot signup twice.
        """
        self.existing_user_payload['confirm_password'] = self.existing_user_payload['password']
        request = self.factory.post(self.user_url, data=self.existing_user_payload, format='json')
        response = self.user_view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['email'][0], 'This email address already exists.')

    def test_password_match(self):
        """
        Ensure password and confirm_password fields are equal.
        """
        request = self.factory.post(self.user_url, data=self.password_mismatch_payload, format='json')
        response = self.user_view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0], 'Passwords don\'t match.')

    def test_user_invite_validation(self):
        """
        Ensure we can signup a new user with valid credentials.
        """
        society = create_fake_society()
        inviter = society.admin
        invitee = get_fake_user()
        serializer = UserInvitationSerializer()
        self.assertEqual(serializer.validate_invite(inviter, invitee), invitee)
        invitee.society = society
        invitee.save()
        self.assertRaises(MemberAlreadyInASocietyException, serializer.validate_invite, inviter, invitee)
        invitee.society = None
        invitee.save()
        fill_up_society(society)
        self.assertRaises(MaximumMembersReachedException, serializer.validate_invite, inviter, invitee)
        empty_society(society)
        create_tenure(society)
        tenure = society.active_tenure
        deadline = get_deadline(tenure)
        self.assertRaises(TenureDeadlinePassedException, serializer.validate_invite, inviter, invitee, deadline)

    def test_validate_user_join(self):
        society = create_fake_society()
        inviter = society.admin
        invitee = get_fake_user()
        serializer = UserInvitationSerializer()
        self.assertEqual(serializer.validate_user_join(inviter, invitee), invitee)
        fill_up_society(society)  # todo: use a custom context manager for this
        self.assertRaises(MaximumMembersReachedException, serializer.validate_user_join, inviter, invitee)
        empty_society(society)
        invitee.society = society
        invitee.save()
        self.assertRaises(MemberAlreadyInASocietyException, serializer.validate_user_join, inviter, invitee)
        invitee.society = None
        invitee.save()
        inviter.society = None
        inviter.save()
        self.assertRaises(SocietyGoneException, serializer.validate_user_join, inviter, invitee)
        inviter.society = society
        inviter.save()
        create_tenure(society)
        tenure = society.active_tenure
        deadline = get_deadline(tenure)
        self.assertRaises(TenureDeadlinePassedException, serializer.validate_user_join, inviter, invitee, deadline)
