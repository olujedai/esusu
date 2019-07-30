from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
	"""
	Custom user model manager where email is the unique identifiers
	for authentication instead of usernames.
	"""
	def create_user(self, email, password, **extra_fields):
		"""
		Create and save a User with the given email and password.
		"""

		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields)
		user.is_active = True
		user.set_password(password)
		user.save()
		return user

	def create_superuser(self, email, password, **extra_fields):
		"""
		Create and save a SuperUser with the given email and password.
		"""
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)
		extra_fields.setdefault('is_active', True)

		if extra_fields.get('is_staff') is not True:
			raise ValueError(_('Superuser must have is_staff=True.'))
		if extra_fields.get('is_superuser') is not True:
			raise ValueError(_('Superuser must have is_superuser=True.'))
		return self.create_user(email, password, **extra_fields)

	def invite_user(self, server_name, inviter, invitee):
		"""
		Send an invite to a user to join your society.
		"""
		from django.core import signing
		import os
		from ..email import send_invite
		SECRET_KEY = os.getenv('SECRET_KEY')
		EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
		EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
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
		# print(email_values)
		send_invite(subject, EMAIL_HOST_USER, invitee.email, **email_values)
		return inviter
