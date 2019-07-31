from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .society import Society


class Tenure(models.Model):
	"""
	Doc string to explan considerations and assumptions.
	"""
	start_date = models.DateField(
		_('Tenure Start Date'),
		help_text=_(
			'Designates the date the tenure starts.'
		),
		null=False,
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
	society = models.ForeignKey(
		Society,
		related_name="tenures",
		on_delete=models.CASCADE
	)

	REQUIRED_FIELDS = ['start_date']
	
	class Meta:
		verbose_name_plural = 'tenure'

	def newest_tenure(self):
		return self.model.objects.order_by('-start_date').first()
