from rest_framework.serializers import ModelSerializer
from ..models import Credit


class CreditSerializer(ModelSerializer):
    class Meta:
        model = Credit
        fields = Credit.FIELDS

    def save(self):
        self.validated_data['contributor'] = self.context['request'].user
        super().save()
