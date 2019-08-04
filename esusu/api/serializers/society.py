from rest_framework import serializers
from ..models import Society
from .society_account import SocietyAccountSerializer
from .user import UserContributionsSerializer
from .tenure import TenureSerializer
import arrow


class SocietySerializer(serializers.ModelSerializer):
	class Meta:
		model = Society
		exclude = ('account')

	def save(self):
		self.validated_data['creator'] = self.context['request'].user
		super().save()

	def get_contributions(self):
		return Society.objects.get_contributions(**self.data)


class SocietyUserSerializer(SocietySerializer):
	account = SocietyAccountSerializer(read_only=True)
	users = UserContributionsSerializer(many=True, read_only=True)


class SocietyTenureSerializer(serializers.ModelSerializer):
	active_tenure = TenureSerializer(read_only=True)
	class Meta:
		model = Society
		exclude = ('account')


