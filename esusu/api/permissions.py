from rest_framework import permissions

class IsAuthenticatedNotPost(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return super(IsAuthenticatedNotPost, self).has_permission(request, view)

class IsASocietyAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_society_admin

class IsInASociety(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.society)

class IsNotInASociety(permissions.BasePermission):
    def has_permission(self, request, view):
        return not bool(request.user.society)