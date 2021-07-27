from django.core.exceptions import ObjectDoesNotExist

from rest_framework import permissions

from .models import CompanyProfile

class IsEmployerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_employer or request.method in permissions.SAFE_METHODS:
            return True
        return False

class IsPositionOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_employer or request.method in permissions.SAFE_METHODS:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        try:
            user_company = CompanyProfile.objects.get(user=request.user)
        except ObjectDoesNotExist:
            return False

        if obj.company == user_company:
            return True
        return False
