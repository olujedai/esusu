import os

from django.conf import settings
from django.core import signing
from rest_framework import serializers, status

from ..email import send_invite
from ..exceptions import (MaximumMembersReachedException,
						  MemberAlreadyInASocietyException,
						  SocietyGoneException, TenureDeadlinePassedException)
from ..models import User
from ..signals import user_joined_society
from .utils import tenure_deadline_passed, this_month, todays_date


class BaseUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		exclude = ('groups', 'user_permissions', 'society', 'last_login', 'is_staff',)
		extra_kwargs = {
			'password': {'write_only': True}
		}

	def create_user(self):
		return User.objects.create_user(**self.validated_data)

	def create_superuser(self):
		return User.objects.create_superuser(**self.validated_data)


class UserInvitationSerializer(serializers.Serializer):

	def validate_invite(self, inviter, invited_user, date=todays_date()):
		if inviter.society.users.count() >= inviter.society.maximum_capacity:
			raise MaximumMembersReachedException(
				detail='Maximum number of users in this society has been reached.',
				status_code='403'
			)
		if tenure_deadline_passed(inviter, date):
			raise TenureDeadlinePassedException(
				detail='The last date for a user to join this group has passed.',
				status_code='403'
			)
		if invited_user.society:
			raise MemberAlreadyInASocietyException(
				detail='This user already belongs to another society',
				status_code='409'
			)
		return invited_user

	def invite_user(self, server_name, inviter, invitee):
		"""
		Send an invite to a user to join your society.
		"""

		SECRET_KEY = settings.SECRET_KEY
		EMAIL_HOST_USER = settings.EMAIL_HOST_USER

		payload = {
			'inviter_id': inviter.id,
			'invitee_id': invitee.id,
		}

		signed_string = signing.dumps(payload, key=SECRET_KEY)
		society_name = inviter.society.name

		subject = f'Join the {society_name} Esusu Society Today'
		email_values = {
			'receiver': invitee,
			'sender': inviter,
			'society_name': society_name,
			'signup_url': f'{server_name}/join/?society={signed_string}',
		}
		send_invite(subject, EMAIL_HOST_USER, invitee.email, **email_values)

	def validate_user_join(self, inviter, invitee, date=todays_date()):
		if not inviter.society:
			raise SocietyGoneException(
				detail='This society does not exist anymore.',
				status_code='410',
			)
		if tenure_deadline_passed(inviter, date):
			raise TenureDeadlinePassedException(
				detail='The last date for a user to join this group has passed.',
				status_code='403'
			)
		if inviter.society.users.count() >= inviter.society.maximum_capacity:
			raise MaximumMembersReachedException(
				detail='The maximum number of users that can join this society has been reached.',
				status_code='410',
			)
		if invitee.society:
			detail = 'You are already a member of this society.'
			if invitee.society != inviter.society:
				detail = 'You already belong to another society.'
			raise MemberAlreadyInASocietyException(
				detail=detail,
				status_code='409',
			)
		return invitee

	def join_society(self, inviter, invitee):
		"""
		Send an invite to a user to join your society.
		"""
		invitee.society = inviter.society
		invitee.save()
		user_joined_society.send(sender=None, user=invitee)


class UserContributionsSerializer(BaseUserSerializer):
	contributions_this_month = serializers.SerializerMethodField()
	all_time_contribution = serializers.SerializerMethodField()

	def get_contributions_this_month(self, user):
		contribution = sum([contribution.amount for contribution in user.contributions.filter(
			date_credited__month__gte=this_month(),
			date_credited__month__lte=this_month()).all()])
		return contribution

	def get_all_time_contribution(self, user):
		contribution = sum([contribution.amount for contribution in user.contributions.all()])
		return contribution


class UserRegistrationSerializer(serializers.ModelSerializer):
	email = serializers.EmailField()
	password = serializers.CharField()
	confirm_password = serializers.CharField()

	class Meta:
		model = User
		fields = ('email', 'password', 'first_name', 'last_name', 'confirm_password')

	def validate_email(self, value):
		email = User.objects.normalize_email(value)
		user = User.objects.filter(email=email).first()
		if user:
			raise serializers.ValidationError(
				"This email address already exists.", 
			)
		return email

	def validate(self, data):
		if not data.get('password') or not data.get('confirm_password'):
			raise serializers.ValidationError("Please enter a password and "
				"confirm it.")
		if data.get('password') != data.get('confirm_password'):
			raise serializers.ValidationError("Passwords don't match.")
		return data
