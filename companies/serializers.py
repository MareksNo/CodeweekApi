from django.conf import settings
from rest_framework import serializers

from .models import CompanyProfile

class CompanyProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyProfile
        fields = ['user', 'company_name', 'position', 'phone_number', 'logo', 'background_photo', 'country', 'company_size', 'location']
        read_only_fields = (['user'])