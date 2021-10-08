from django.db import models
from django.db.models import fields
from django.forms.models import model_to_dict

from rest_framework import serializers

from .models import JobOffer, UserModel, JobSeekerProfile

from core.serilaizers import OccupationSerializer

from companies.serializers import CompanyProfileSerializer
from companies.models import CompanyProfile

class RegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = UserModel
        fields = ['email', 'password', 'password2', 'is_employer', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = UserModel(
            email=self.validated_data['email'],
            is_employer=self.validated_data['is_employer'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords not matching!'})
        user.set_password(password)
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['id', 'email', 'is_employer', 'first_name', 'last_name', 'has_premium']
        read_only_fields = (['is_employer', 'id', 'has_premium'])


class SearchUserSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()
    class Meta:
        model = UserModel
        fields = ['id', 'email', 'is_employer', 'first_name', 'last_name', 'profile', 'has_premium']
        read_only_fields = (['is_employer', 'id', 'has_premium'])

    def get_profile(self, obj):
        if not obj.is_employer:
            profile = JobSeekerProfile.objects.get(user=obj)
            profile_dict = model_to_dict(profile)
            
            if not profile_dict['photo']:
                profile_dict['photo'] = ''
            else:
                profile_dict['photo'] = profile.photo.url

            return profile_dict
        else:
            profile = CompanyProfile.objects.get(user=obj)
            profile_dict = model_to_dict(profile)
            if not profile_dict['background_photo']:
                profile_dict['background_photo'] = ''
            else:
                profile_dict['background_photo'] = profile.background_photo.url

            if not profile_dict['logo']:
                profile_dict['logo'] = ''
            else:
                profile_dict['logo'] = profile.logo.url
            
            return profile_dict 



class JobSeekerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSeekerProfile
        fields = ['id', 'user', 'photo', 'birth_date', 'country', 'city', 'interests', 'experience', 'languages', 'knowledge', 'extra', 'profession_aka_activity', 'is_active_jobseeker', 'bio']
        read_only_fields = (['user', 'id'])


class JobOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobOffer
        fields = ['id', 'user_profile', 'job_title', 'skills', 'knowledge', 'info', 'contract_type', 'post_time']
        read_only_fields = (['user_profile', 'post_time', 'id'])


# class ReviewSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Review
#         fields = ['id', 'company', 'jobseeker', 'text', 'rating', 'review_time']
#         read_only_fields = (['review_time', 'id', 'company', 'jobseeker'])
