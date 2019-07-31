from rest_framework import permissions


class IsASocietyAdmin(permissions.BasePermission):
	def has_permission(self, request, view):
		return request.user.is_society_admin


class IsInASociety(permissions.BasePermission):
	def has_permission(self, request, view):
		return bool(request.user.society)


class IsNotInASociety(permissions.BasePermission):
	def has_permission(self, request, view):
		return not bool(request.user.society)


class IsSudoUser(permissions.BasePermission):
	"""
	Allow only POST requests.
	"""
	def has_permission(self, request, view):
		return request.user.is_superuser