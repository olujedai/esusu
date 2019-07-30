from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from ..manager import CollectionScheduleManager
from .tenure import Tenure
from .user import User


class CollectionSchedule(models.Model):
	user = models.ForeignKey(
		User,
        related_name='collection_schedules',
		on_delete=models.CASCADE,
	)
	collection_date = models.DateField(
		_('Collection Date'),
		help_text=_(
			'Designates the date that this user will be \
                eligible to collect the contribution from the society.'
		),
	)
    tenure = models.ForeignKey(
        Tenure,
        related_name="collection_schedule",
        on_delete=models.CASCADE
    )

	objects = CollectionScheduleManager()
	
	class Meta:
		verbose_name_plural = 'collection_schedules'
