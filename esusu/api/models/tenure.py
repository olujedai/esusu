from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from ..manager import TenureManager


class Tenure(models.Model):
	start_date = models.DateField(
		_('Tenure Start Date'),
		help_text=_(
			'Designates the date the tenure starts.'
		),
	)
	tentative_end_date = models.DateField(
		_('Tentative End Date'),
		help_text=_(
			'Designates the date a tenure will end if the maximum \
				capacity of the society has not been reached. It also \
					represents the last date a member can join the Esusu Society.'
		),
	)
	maximum_end_date = models.DateField(
		_('Maximum End Date'),
		help_text=_(
			'Designates the date a tenure will end once the maximum \
					capacity of the society has been reached.'
		),
	)
	

	objects = TenureManager()
	
	class Meta:
		verbose_name_plural = 'tenure'
