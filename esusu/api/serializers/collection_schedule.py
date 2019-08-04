from rest_framework import serializers

from ..models import CollectionSchedule
from .user import BaseUserSerializer


class CollectionScheduleSerializer(serializers.ModelSerializer):
	user = BaseUserSerializer(read_only=True)
	class Meta:
		model = CollectionSchedule
		fields = '__all__'
		extra_kwargs = {
			'tenure': {'write_only': True},
		}
