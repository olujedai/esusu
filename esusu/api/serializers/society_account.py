from rest_framework.serializers import ModelSerializer
from ..models.society_account import SocietyAccount


class SocietyAccountSerializer(ModelSerializer):
    class Meta:
        model = SocietyAccount
        fields = '__all__'
