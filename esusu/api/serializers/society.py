from rest_framework.serializers import ModelSerializer
from ..models import Society
from .society_account import SocietyAccountSerializer
from .user import UserContributionsSerializer

class SocietySerializer(ModelSerializer):
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

class SocietyDetailsSerializer(SocietyUserSerializer):
    pass