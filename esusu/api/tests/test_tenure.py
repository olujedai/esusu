from django.urls import path
from rest_framework import status, serializers
from rest_framework.test import (APIRequestFactory, APITestCase,
                                 force_authenticate)

from api.exceptions import (MaximumMembersReachedException,
                            MemberAlreadyInASocietyException,
                            SocietyGoneException,
                            TenureDeadlinePassedException)
from api.models import User
from api.serializers import TenureSerializer, UserInvitationSerializer
from api.views import InviteUserToSocietyView, UserView

from .utils import (create_fake_society, create_tenure, empty_society,
                    fill_up_society, get_auth_token, get_deadline,
                    get_fake_user)
import arrow
from ..handlers import get_new_tentative_end_date


class TenureTests(APITestCase):

    def test_tenure_creation(self):
        """
        Ensure we can signup a new user with valid credentials.
        """
        society = create_fake_society()
        inviter = society.admin
        self.assertIsNone(society.active_tenure)
        now = arrow.now('Africa/Lagos').date()
        tenure = create_tenure(society, when=now)
        self.assertIsNotNone(society.active_tenure)
        self.assertEqual(society.active_tenure, tenure)
        serializer = TenureSerializer()
        serializer.society = society
        # duplicate tenure
        self.assertRaises(serializers.ValidationError, serializer.validate_start_date, now)
        tenure.delete()

        past = arrow.now('Africa/Lagos').shift(days=-1).date()
        # tenure in the past
        self.assertRaises(serializers.ValidationError, serializer.validate_start_date, past)
        
        future = arrow.now('Africa/Lagos').shift(days=2).date()
        tenure = create_tenure(society, when=future)
        # Conflicting tenure
        self.assertRaises(serializers.ValidationError, serializer.validate_start_date, now)
        tenure.delete()

        tenure = create_tenure(society)
        when = get_deadline(tenure)
        # Test Cannot start a new tenure during an active tenure
        self.assertRaises(serializers.ValidationError, serializer.validate_start_date, when)

    def test_tenure_update_after_user_join(self):
        society = create_fake_society()
        tenure = create_tenure(society)
        inviter = society.admin
        invitee = get_fake_user()
        self.assertIsNone(invitee.society)
        old_tentative_end_date = tenure.tentative_end_date
        new_tentative_end_date = get_new_tentative_end_date(tenure.tentative_end_date)
        last_schedule_before_new_user_joined = tenure.collection_schedules.order_by('-id').first()
        UserInvitationSerializer().join_society(inviter, invitee)
        self.assertIsNotNone(invitee.society)
        self.assertEqual(invitee.society, society)
        tenure.refresh_from_db()
        # new member is last collector
        last_schedule_after_new_user_joined = tenure.collection_schedules.order_by('-id').first()
        self.assertTrue(last_schedule_after_new_user_joined.id > last_schedule_before_new_user_joined.id)
        self.assertNotEqual(old_tentative_end_date, new_tentative_end_date)
        self.assertEqual(tenure.tentative_end_date, new_tentative_end_date)
