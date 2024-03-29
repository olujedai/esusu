import arrow
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from ..manager import SocietyManager
from .society_account import SocietyAccount


class Society(models.Model):
	name = models.CharField(
		_('society name'),
		max_length=150,
		unique=True,
		help_text=_(
			'Designates the name of the society.'
		),
	)
	description = models.CharField(
		_('description'),
		max_length=300,
		help_text=_(
			'A description of the society.'
		),
	)
	maximum_capacity = models.IntegerField(
		_('maximum capacity'),
		help_text=_(
			'Designates the maximum number people that can be in the society.'
		),
	)
	periodic_amount = models.IntegerField(
		_('periodic amount'),
		help_text=_(
			'Designates the weekly amount to be contributed by the members of this savings society.'
		),
	)
	is_searchable = models.BooleanField(
		default=False,
		help_text=_(
			'Designates whether this savings society is public or not. '
		),
	)
	date_created = models.DateTimeField(default=timezone.now)
	account = models.OneToOneField(
		SocietyAccount,
		on_delete=models.CASCADE,
		# primary_key=True,
	)


	REQUIRED_FIELDS = ['name', 'description', 'maximum_capacity', 'periodic_amount', 'is_searchable']

	objects = SocietyManager()
	
	class Meta:
		verbose_name_plural = 'societies'

	@property
	def active_tenure(self):
		todays_date = arrow.now('Africa/Lagos').date()
		return self.tenures.filter(
			start_date__lte=todays_date,
			maximum_end_date__gte=todays_date,
		).first()
	
	@property
	def admin(self):
		society_admin = {
			'admin': None
		}
		if not society_admin['admin']:
			society_admin['admin'] = self.users.filter(is_society_admin=True).first()
		return society_admin['admin']
