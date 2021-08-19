from django.conf import settings
from rest_framework import serializers

from .models import CompanyProfile, Position

class CompanyProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyProfile
        fields = ['id', 'user', 'company_name', 'position', 'phone_number', 'logo', 'background_photo', 'country', 'company_size', 'country', 'city']
        read_only_fields = (['id', 'user'])

class PositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Position
        fields = ['id', 'company', 'position_occupation', 'position_info', 'position_tools', 'position_city', 'position_country', 'position_languages', 'position_requirements', 'price_range', 'contract_type', 'post_time']
        read_only_fields = (['company', 'post_time', 'id'])
