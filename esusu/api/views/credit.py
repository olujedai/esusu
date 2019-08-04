from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from ..models import Credit
from ..permissions import IsInASociety
from ..serializers import CreditSerializer


class NewCreditView(generics.CreateAPIView):
	"""
	Make a contribution.
	"""
	permission_classes = (IsAuthenticated, IsInASociety,)
	queryset = Credit.objects.all()
	serializer_class = CreditSerializer
