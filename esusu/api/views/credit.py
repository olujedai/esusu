from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from ..models import Credit
from ..serializers import CreditSerializer
from ..permissions import IsInASociety


class NewCreditView(generics.CreateAPIView):
	"""
	Make a contribution.
	"""
	permission_classes = (IsAuthenticated, IsInASociety,)
	queryset = Credit.objects.all()
	serializer_class = CreditSerializer
