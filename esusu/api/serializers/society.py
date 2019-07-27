from rest_framework.serializers import ModelSerializer
from ..models import Society
from .user import UserSerializer


class SocietySerializer(ModelSerializer):
    users = UserSerializer(many=True, read_only=True)
    class Meta:
        model = Society
        fields = '__all__'

    def save(self):
        self.validated_data['creator'] = self.context['request'].user
        super().save()