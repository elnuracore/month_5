from rest_framework.permissions import BasePermission

class IsModerator(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return False
        if not request.user.is_staff:
            return False
        if not request.user or not request.user.is_authenticated:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return request.method in ['GET', 'PUT', 'DELETE', 'PATCH']
        return False
    

        
