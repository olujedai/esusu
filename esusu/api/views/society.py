from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from ..models import Society, User
from ..serializers import SocietySerializer
from rest_framework.permissions import IsAuthenticated


class SocietyView(generics.ListCreateAPIView):
	"""
	List all cooperative societies, create a new society.
	"""
	permission_classes = (IsAuthenticated,)
	queryset = Society.objects.filter(is_searchable=True).all()
	serializer_class = SocietySerializer


class SocietyDetail(generics.RetrieveUpdateDestroyAPIView):
	"""
	Edit, Delete or Retrieve the details of one society.
	"""
	queryset = Society.objects.all()
	serializer_class = SocietySerializer

class MySociety(generics.RetrieveUpdateDestroyAPIView):
	"""
	Edit, Delete or Retrieve the details of my society.
	"""
	permission_classes = (IsAuthenticated,)
	# queryset = Society.objects.all()
	# serializer_class = SocietySerializer
	# lookup_field = 'email'

	def retrieve(self, request):
		queryset = User.objects.filter(email=self.request.user.email).first()
		if not queryset or not hasattr(queryset, 'society'):
			return Response({'message': 'Society not found'}, status=status.HTTP_404_NOT_FOUND)
		return Response(SocietySerializer(queryset.society).data, status=status.HTTP_200_OK)

	def update(self, request):
		queryset = User.objects.filter(email=self.request.user.email).first()
		if not queryset or not hasattr(queryset, 'society'):
			return Response({'message': 'Society not found'}, status=status.HTTP_404_NOT_FOUND)
		model_serializer = SocietySerializer(data=request.data)
		model_serializer.is_valid(raise_exception=True)
		data = model_serializer.create()
		return Response(SocietySerializer(queryset.society).data, status=status.HTTP_201_CREATED)


class SearchSocietiesView(generics.ListAPIView):
	"""
	Search for societies to join.
	"""
	serializer_class = SocietySerializer

	def get_queryset(self):
		"""
		Optionally restricts the returned societies,
		by filtering against a society `name` query parameter in the URL.
		"""
		queryset = Society.objects.filter(is_searchable=True).all()
		name = self.request.query_params.get('name', None)
		if name is not None:
			queryset = queryset.filter(name__unaccent__icontains=name)
		return queryset
