# creating permissions for users
from rest_framework.permissions import BasePermission, SAFE_METHODS


# Permissions classes
# checks whether the user has the permission to perform the
# the specified action
class UserPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return request.method in SAFE_METHODS
        if view.basename in ['posts']:
            return bool(request.user and request.user.is_authenticated)
        return False
    
    def has_permission(self, request, view):
        if view.basename in ['post']:
            if request.user.is_anonymous:
                return bool(request.user and request.user.is_authenticated)
        return False
    
