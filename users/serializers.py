from django.db import models
from rest_framework import serializers

from .models import JobOffer, UserModel, JobSeekerProfile

from core.serilaizers import OccupationSerializer

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


class JobSeekerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSeekerProfile
        fields = ['id', 'user', 'photo', 'age', 'location', 'interests', 'experience', 'languages', 'knowledge', 'extra', 'profession_aka_activity']
        read_only_fields = (['user', 'id'])


class JobOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobOffer
        fields = ['id', 'user_profile', 'job_title', 'skills', 'knowledge', 'info', 'contract_type', 'post_time']
        read_only_fields = (['user_profile', 'post_time', 'id'])

