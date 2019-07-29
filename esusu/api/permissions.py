from rest_framework import permissions

class IsAuthenticatedNotPost(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return super(IsAuthenticatedNotPost, self).has_permission(request, view)

class IsSocietyAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_society_admin

class IsInAGroup(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.society)
