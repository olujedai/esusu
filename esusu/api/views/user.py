from django.conf import settings
from django.core import signing
from django.http import Http404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..exceptions import CustomException
from ..models import User
from ..permissions import IsASocietyAdmin, IsSudoUser
from ..serializers import BaseUserSerializer, UserRegistrationSerializer, UserInvitationSerializer


class UserSignUpView(generics.CreateAPIView):
	permission_classes = []
	serializer_class = BaseUserSerializer
	def post(self, request, format=None):
		"""
		Create a new user
		"""
		serializer = UserRegistrationSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		model_serializer = BaseUserSerializer(data=request.data)
		model_serializer.is_valid(raise_exception=True)
		data = model_serializer.create_user()
		return Response(BaseUserSerializer(data).data, status=status.HTTP_201_CREATED)


class UserView(generics.ListAPIView):
	"""
	List all users, or create a new user.
	"""
	permission_classes = [IsAuthenticated, IsSudoUser]
	serializer_class = BaseUserSerializer

	def get(self, request, format=None):
		"""
		List all users
		"""
		users = User.objects.all()
		serializer = BaseUserSerializer(users, many=True)
		return Response(serializer.data)


class InviteUserToSocietyView(generics.UpdateAPIView):
	"""
	Invite a user to a view.
	"""
	permission_classes = (IsAuthenticated, IsASocietyAdmin,)
	serializer_class = UserInvitationSerializer

	def get_object(self, pk):
		try:
			return User.objects.get(pk=pk)
		except User.DoesNotExist:
			raise Http404

	def update(self, request, pk):
		invited_user = self.get_object(pk)
		inviter = request.user
		UserInvitationSerializer().validate_invite(inviter, invited_user)
		server_name = request.META['HTTP_HOST']
		UserInvitationSerializer().invite_user(server_name, inviter, invited_user)
		return Response({'message': 'User invite sent.'}, status=status.HTTP_202_ACCEPTED)


class JoinSocietyView(generics.RetrieveAPIView):
	"""
	View to handle user's accepting the invite.
	"""
	serializer_class = UserInvitationSerializer

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
		inviter = self.get_object(society_params['inviter_id'])
		invitee = self.get_object(society_params['invitee_id'])
		UserInvitationSerializer().validate_user_join(inviter, invitee)
		UserInvitationSerializer().join_society(inviter, invitee)
		return Response({'message': 'Success.'}, status=status.HTTP_200_OK)
