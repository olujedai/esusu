from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, AbstractUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .society import Society
from ..manager import UserManager
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField(_('email address'), unique=True)
	first_name = models.CharField(_('first name'), max_length=30, blank=True)
	last_name = models.CharField(_('last name'), max_length=150, blank=True)

	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)
	is_society_admin = models.BooleanField(default=False)
	is_active = models.BooleanField(
		default=True,
		help_text=_(
			'Designates whether this user should be treated as active. '
			'Unselect this instead of deleting accounts.'
		),
	)
	date_joined = models.DateTimeField(default=timezone.now)
	society = models.ForeignKey(Society, related_name="users", null=True, on_delete=models.SET_NULL)  # A user does not have to belong to a savings society.

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['first_name', 'last_name', 'password']

	objects = UserManager()

	@property
	def full_name(self):
		return f'{self.first_name} {self.last_name}'
