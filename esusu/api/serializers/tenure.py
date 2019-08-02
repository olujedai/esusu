from datetime import datetime
from itertools import count
from random import shuffle

import arrow
from rest_framework import serializers

from ..models import CollectionSchedule, Tenure
from .collection_schedule import CollectionScheduleSerializer
from .utils import get_max_end_date_time, in_the_past, shift_by


class TenureSerializer(serializers.ModelSerializer):
	collection_schedules = CollectionScheduleSerializer(many=True, read_only=True)
	start_date = serializers.DateField()

	class Meta:
		model = Tenure
		exclude = ('society',)
		extra_kwargs = {
			'tentative_end_date': {'read_only': True},
			'maximum_end_date': {'read_only': True},
		}

	def validate_start_date(self, value):
		if in_the_past(value):
			raise serializers.ValidationError(
				"A tenure start date cannot be in the past.", 
			)

		try:
			society = self.context['request'].user.society
		except KeyError:  # todo: hack for tests to pass. look into request mocking
			society = self.society
		newest_tenure = society.tenures.order_by('-start_date').first()
		if newest_tenure:
			if value == newest_tenure.start_date:
				raise serializers.ValidationError(
					"A tenure with this start date already exists.", 
				)
			is_before_newest_tenure = value < newest_tenure.start_date
			is_after_newest_tenure = value > newest_tenure.start_date
			is_before_maximum_end_date = value < newest_tenure.maximum_end_date
			if is_before_newest_tenure:
				raise serializers.ValidationError(
					"A tenure currently exists.", 
				)
			if is_after_newest_tenure and is_before_maximum_end_date:
				raise serializers.ValidationError(
					"Cannot start a new tenure during an active tenure.", 
				)
		return value

	def save(self):
		start_date = self.validated_data['start_date']
		try:
			society = self.context['request'].user.society
		except KeyError:  # todo: hack for tests to pass. look into request mocking
			society = self.society
		setup_tenure(society, start_date)


def setup_tenure(society, start_date):
	start_date_time = arrow.get(start_date, 'Africa/Lagos')
	users = list(society.users.all())
	shuffle(users)
	contribution_maturity_period_in_weeks = 4  # todo: make this configurable during tenure creation.
	counter = count(start=contribution_maturity_period_in_weeks, step=contribution_maturity_period_in_weeks) 
	collection_date_times = [shift_by(start_date_time, next(counter)) for user in users]
	number_of_users = len(users)  # According to the documentation at: https://docs.djangoproject.com/en/dev/ref/models/querysets/#django.db.models.query.QuerySet.count this is more efficient than calling count() since we will load all() the users from memory anyway 
	maximum_end_date_time = tentative_end_date_time = collection_date_times[-1]
	if number_of_users < society.maximum_capacity:
		maximum_end_date_time = get_max_end_date_time(start_date_time, society.maximum_capacity)
	new_tenure = Tenure(
		start_date=start_date,
		tentative_end_date=tentative_end_date_time.date(),
		maximum_end_date=maximum_end_date_time.date(),
		society=society,
	)
	new_tenure.save()
	schedules = [
		CollectionSchedule(
			user=user,
			collection_date=collection_date_time.date(),
			tenure=new_tenure,
		) for user, collection_date_time in zip(users, collection_date_times)
	]
	CollectionSchedule.objects.bulk_create(schedules)
