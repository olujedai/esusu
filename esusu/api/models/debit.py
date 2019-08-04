from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .society_account import SocietyAccount
from .user import User


class Debit(models.Model):
	"""
	This model represents the debits made from a `SocietyAccount` to a `User`.
	While from the view of the `Society`, it is a debit, the receiving user views this as a `collection`.
	For more on this, see http://in-formality.com/wiki/index.php?title=Esusu_(Nigeria)
	"""
	amount = models.IntegerField(
		_('Amount'),
		help_text=_(
			'Designates the amount of money debited from the society\'s account.'
		),
	)
	date_debited = models.DateTimeField(
		_('Date'),
		default=timezone.now,
		help_text=_(
			'The date a debit was made.'
		),
	)
	user = models.ForeignKey(User, related_name="collections", on_delete=models.CASCADE)
	account = models.ForeignKey(SocietyAccount, related_name="debits", on_delete=models.CASCADE)
