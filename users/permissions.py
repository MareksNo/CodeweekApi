from django.core.exceptions import ObjectDoesNotExist

from rest_framework import permissions

from .models import JobSeekerProfile

class IsJobSeekerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and not request.user.is_employer or request.method in permissions.SAFE_METHODS:
            return True
        return False
