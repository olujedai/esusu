from rest_framework import generics, status
from rest_framework.response import Response


class IndexView(generics.RetrieveAPIView):
	permission_classes = []

	def get(self, request, format=None):
		"""
		Welcome message
		"""
		return Response({'message': 'Welcome to the Esusu API. The documentation of this api can be found at https://github.com/olujedai/esusu/blob/master/ENDPOINTS.md'}, status=status.HTTP_200_OK)
