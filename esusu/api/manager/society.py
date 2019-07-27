from django.utils.translation import gettext_lazy as _
from django.db import models


class SocietyManager(models.Manager):

	def create(self, **data):
		"""
		Create and save a Society and make the creator the administrator.
		"""
		user = data['creator']
		del data['creator']
		society = self.model(**data)
		society.save()
		user.society = society
		user.is_society_admin = True
		user.save()
		return society
