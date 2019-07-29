from django.http import Http404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import Society, User
from ..permissions import IsASocietyAdmin
from ..serializers import SocietySerializer, SocietyUserSerializer
from ..exceptions import CustomException


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
	permission_classes = (IsAuthenticated,)
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


class SocietyContributions(generics.RetrieveAPIView):
	"""
	Edit, Delete or Retrieve the details of my society.
	"""
	permission_classes = (IsAuthenticated, IsASocietyAdmin,)

	def retrieve(self, request):
		return Response(SocietyUserSerializer(request.user.society).data, status=status.HTTP_200_OK)


class InviteUserToSocietyView(generics.UpdateAPIView):
	"""
	Invite a user to a view.
	"""
	permission_classes = (IsAuthenticated, IsASocietyAdmin,)
	serializer_class = SocietySerializer

	def get_object(self, pk):
		try:
			return User.objects.get(pk=pk)
		except User.DoesNotExist:
			raise Http404

	def update(self, request, pk):
		invited_user = self.get_object(pk)
		if invited_user.society:
			raise CustomException(
				detail='This user already belongs to another society',
				status_code='409'
			)
		User.objects.invite_user(invited_user)
		return Response({'message': 'User successfully invited.'}, status=status.HTTP_200_OK)
