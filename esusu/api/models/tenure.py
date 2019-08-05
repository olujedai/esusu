import arrow
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .society import Society


class Tenure(models.Model):
	"""
    During the design of the Tenure Model, a few assumptions and contraints were made based on the 
    specifications, user stories and after studying the suggested Esusu literature.

    ASSUMPTIONS
    -   A tenure can start if the maximum_capacity of the Society hasn't been reached.
    -   When a new user joins, the user is added to the CollectionSchedule of the Tenure and will be the last person to collect.

    OBSERVATION
    -   A user joining after a tenure starts means that user will collect more money than other members who joined earlier in the Tenure and have already collected.

    PROPOSED SOLUTION
    -   Prevent a user from joining or leaving a society once a tenure has started.
        This will ensure everyone will collect the same amount of money throughout the Tenure duration. However, implementing the Tenure class with this 
        solution conflicts with the Specifications and User Stories.

    IMPLEMENTATION
    -   The tenure has a start date (specified by the Society's Admin) and two end dates - The 'tentative_end_date' and the 'maximum_end_date'.
    -   Tentative end date: This is the date a tenure will end if the maximum capacity of the society has not been reached. It also represents
                         the last date a member can join the Esusu Society.
    -   Maximum end date: This is the date a tenure will end if the maximum capacity of the society is reached before a tentative end date lapses.
    -   When a new user joins the society, the user is added to the bottom of the collection schedule and the tentative end date is adjusted
        to become the collection date of this new user.
    -   A user can only join a society if the tentative end date of the society has not been reached at the time the user signs up.
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

	def is_active(self):
		todays_date = arrow.now('Africa/Lagos').date()
		return todays_date > self.start_date and todays_date <= self.tentative_end_date

	def starts_soon(self):
		todays_date = arrow.now('Africa/Lagos').date()
		return todays_date <= self.start_date
