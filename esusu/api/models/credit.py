from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .society_account import SocietyAccount
from .user import User
from ..manager import CreditManager


class Credit(models.Model):
	"""
	This model represents the credits made from to the `SocietyAccount` by a `User`.
	These credits are counted as `contributions` by a `User`.
	For more on this, see http://in-formality.com/wiki/index.php?title=Esusu_(Nigeria)
	"""
	amount = models.IntegerField(
		_('Amount'),
		default=0,
		help_text=_(
			'Designates the amount of money credited to an account.'
		),
	)
	date_credited = models.DateTimeField(
		_('Date'),
		default=timezone.now,
		help_text=_(
			'The date a credit was made.'
		),
	)
	contributor = models.ForeignKey(User, related_name="contributions", on_delete=models.CASCADE)
	account = models.ForeignKey(SocietyAccount, related_name="credits", on_delete=models.CASCADE)

	FIELDS = ['amount', 'date_credited']
	objects = CreditManager()
