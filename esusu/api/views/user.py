from django.conf import settings
from django.core import signing
from django.http import Http404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..exceptions import CustomException
from ..models import User
from ..permissions import IsASocietyAdmin
from ..serializers import BaseUserSerializer, UserRegistrationSerializer, UserInvitationSerializer


class UserView(APIView):
	"""
	List all users, or create a new snippet.
	"""
	def get(self, request, format=None):
		users = User.objects.all()
		serializer = BaseUserSerializer(users, many=True)
		return Response(serializer.data)

	def post(self, request, format=None):
		serializer = UserRegistrationSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		model_serializer = BaseUserSerializer(data=request.data)
		model_serializer.is_valid(raise_exception=True)
		data = model_serializer.create_user()
		return Response(BaseUserSerializer(data).data, status=status.HTTP_201_CREATED)


class InviteUserToSocietyView(generics.UpdateAPIView):
	"""
	Invite a user to a view.
	"""
	permission_classes = (IsAuthenticated, IsASocietyAdmin,)

	def get_object(self, pk):
		try:
			return User.objects.get(pk=pk)
		except User.DoesNotExist:
			raise Http404

	def update(self, request, pk):
		invited_user = self.get_object(pk)
		inviter = request.user
		server_name = request.META['HTTP_HOST']
		UserInvitationSerializer().invite_user(server_name, inviter, invited_user)
		return Response({'message': 'User invite sent.'}, status=status.HTTP_202_ACCEPTED)


class JoinSocietyView(generics.RetrieveAPIView):
	"""
	View to handle user's accepting the invite.
	"""

	def get_object(self, pk):
		try:
			return User.objects.get(pk=pk)
		except User.DoesNotExist:
			raise Http404

	def retrieve(self, request):
		society = request.query_params.get('society', None)
		if not society:
			raise CustomException(
				detail='Signature missing.',
				status_code='404'
			)
		try:
			society_params = signing.loads(society, key=settings.SECRET_KEY)
		except signing.BadSignature:
			raise CustomException(
				detail='Bad signature',
				status_code='400'
			)
		UserInvitationSerializer().join_society(**society_params)
		return Response({'message': 'Success.'}, status=status.HTTP_200_OK)
