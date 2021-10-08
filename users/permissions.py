from django.core.exceptions import ObjectDoesNotExist

from rest_framework import permissions

from companies.models import CompanyProfile

from .models import JobSeekerProfile

class IsJobSeekerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and not request.user.is_employer or request.method in permissions.SAFE_METHODS:
            return True
        return False

class IsJobOfferOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and not request.user.is_employer or request.method in permissions.SAFE_METHODS:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        try:
            user_profile = JobSeekerProfile.objects.get(user=request.user)
        except ObjectDoesNotExist:
            return False

        if obj.user_profile == user_profile:
            return True
        return False


class UserIsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_superuser:
            return True

        return obj.id == request.user.id


# class IsVerifiedCompany(permissions.BasePermission):
#     def has_permission(self, request, view):
#         if request.method in permissions.SAFE_METHODS:
#             return True

#         if request.user.is_superuser:
#             return True

#         if request.user.is_employer:
#             try:
#                 company_profile = CompanyProfile.objects.get(user=request.user)
#             except ObjectDoesNotExist:
#                 return False
            
#             return company_profile.is_verified
