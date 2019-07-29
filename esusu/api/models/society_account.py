from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class SocietyAccount(models.Model):
	balance = models.IntegerField(
		_('Amount'),
		default=0,
		help_text=_(
			'Designates the amount of money in the society\'s account.'
		),
	)
	date_created = models.DateTimeField(
		_('Date'),
		default=timezone.now,
		help_text=_(
			'The date the account was created.'
		),
	)
