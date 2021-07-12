from django.db import models
from rest_framework import serializers

from .models import UserModel, JobSeekerProfile

class RegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = UserModel
        fields = ['email', 'username', 'password', 'password2', 'is_employer', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = UserModel(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
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
        fields = ['user', 'photo', 'age', 'location', 'interests', 'experience', 'languages', 'knowledge', 'extra']



    # photo = models.ImageField(upload_to='user_photos/', blank=True)
    # age = models.IntegerField(validators=[MaxValueValidator(123)], null=True, blank=True)
    # location = models.TextField(max_length=900, blank=True)
    # interests = models.TextField(max_length=3000, default='', blank=True)
    # experience = models.TextField(max_length=3000, default='', blank=True)
    # languages = models.TextField(max_length=1500, default='', blank=True)
    # knowledge = models.TextField(max_length=3000, default='', blank=True)
    # extra = models.TextField(max_length=3000, default='', blank=True)