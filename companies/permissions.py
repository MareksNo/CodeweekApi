from rest_framework import permissions

class IsEmployerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        
        if request.user.is_authenticated and request.user.is_employer or request.method in permissions.SAFE_METHODS:
            return True
        return False

