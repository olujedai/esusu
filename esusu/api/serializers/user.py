from rest_framework import serializers, status
from ..models import User
from .utils import in_this_month


class BaseUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		exclude = ('groups', 'user_permissions', 'society')
		extra_kwargs = {
			'password': {'write_only': True}
		}

	def create_user(self):
		print(self.validated_data)
		return User.objects.create_user(**self.validated_data)

	def create_superuser(self):
		return User.objects.create_superuser(**self.validated_data)


class UserContributionsSerializer(BaseUserSerializer):
	contributions_this_month = serializers.SerializerMethodField()
	all_time_contribution = serializers.SerializerMethodField()

	def get_contributions_this_month(self, user):
		contribution = sum([contribution.amount for contribution in user.contributions.all() if in_this_month(contribution.date_credited)])
		return contribution

	def get_all_time_contribution(self, user):
		contribution = sum([contribution.amount for contribution in user.contributions.all()])
		return contribution


class UserRegistrationSerializer(serializers.Serializer):
	email = serializers.EmailField()
	password = serializers.CharField()
	confirm_password = serializers.CharField()

	def validate_email(self, value):
		email = User.objects.normalize_email(value)
		user = User.objects.filter(email=email).first()
		if user:
			raise serializers.ValidationError(
				"This email address already exists.", 
			)
		return email

	def validate(self, data):
		if not data.get('password') or not data.get('confirm_password'):
			raise serializers.ValidationError("Please enter a password and "
				"confirm it.")
		if data.get('password') != data.get('confirm_password'):
			raise serializers.ValidationError("Passwords don't match.")
		return data
