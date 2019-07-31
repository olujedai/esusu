from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import Tenure
from ..serializers import TenureSerializer
from ..permissions import IsASocietyAdmin


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

	# def retrieve(self, request):
	# 	return Response(TenureSerializer(request.user.society).data, status=status.HTTP_200_OK)

	def get_queryset(self):
		return self.request.user.society.tenures.order_by('-start_date').first()