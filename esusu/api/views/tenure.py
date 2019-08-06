from django.http import Http404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import Tenure
from ..permissions import IsASocietyAdmin
from ..serializers import TenureSerializer


class NewTenureView(generics.ListCreateAPIView):
	"""
	Make a contribution.
	"""
	permission_classes = (IsAuthenticated, IsASocietyAdmin,)
	serializer_class = TenureSerializer

	def get_queryset(self):
		return Tenure.objects.filter(society=self.request.user.society).all()


class TenureDetail(generics.RetrieveAPIView):
	"""
	Edit, Delete or Retrieve the details of my society.
	"""
	permission_classes = (IsAuthenticated, IsASocietyAdmin,)
	serializer_class = TenureSerializer

	def get_object(self, pk):
		try:
			return Tenure.objects.get(pk=pk)
		except Tenure.DoesNotExist:
			raise Http404

	def retrieve(self, _, pk):
		tenure = self.get_object(pk)
		return Response(TenureSerializer(tenure).data, status=status.HTTP_200_OK)
