from rest_framework import serializers
from ..models import Society
from .society_account import SocietyAccountSerializer
from .user import UserContributionsSerializer
from .tenure import TenureSerializer
import arrow


class SocietySerializer(serializers.ModelSerializer):
	account = SocietyAccountSerializer(read_only=True)
	class Meta:
		model = Society
		fields = '__all__'

	def save(self):
		self.validated_data['creator'] = self.context['request'].user
		super().save()

	def get_contributions(self):
		return Society.objects.get_contributions(**self.data)


class SocietyUserSerializer(SocietySerializer):
	users = UserContributionsSerializer(many=True, read_only=True)


class SocietyTenureSerializer(serializers.ModelSerializer):
	active_tenure = TenureSerializer(read_only=True)
	class Meta:
		model = Society
		fields = '__all__'


