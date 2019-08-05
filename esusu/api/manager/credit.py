from django.db import models
from django.utils.translation import gettext_lazy as _

from ..models.society_account import SocietyAccount


class CreditManager(models.Manager):

	def create(self, **data):
		"""
		Create and save a Credit.
		"""
		contributor = data['contributor']
		account = contributor.society.account
		if not account:
			account = SocietyAccount()
			account.save()
			contributor.society.account = account
			data['account'] = account
		account.balance += data['amount']
		account.save()
		data['account'] = account
		credit = self.model(**data)
		credit.save()
		return credit
