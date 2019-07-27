from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from ..manager import SocietyManager


class Society(models.Model):
	name = models.CharField(
		_('society name'),
		max_length=150,
		unique=True,
		help_text=_(
			'Designates the name of the group.'
		),
	)
	description = models.CharField(
		_('description'),
		max_length=300,
		help_text=_(
			'A description of the group.'
		),
	)
	maximum_capacity = models.IntegerField(
		_('maximum capacity'),
		help_text=_(
			'Designates the maximum number people that can be in the group.'
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


	REQUIRED_FIELDS = ['name', 'description', 'maximum_capacity', 'periodic_amount', 'is_searchable']

	objects = SocietyManager()
	
	class Meta:
		verbose_name_plural = 'societies'
