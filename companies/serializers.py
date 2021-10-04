from django.conf import settings
from rest_framework import serializers

from .models import CompanyProfile, Match, Position

class CompanyProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyProfile
        fields = ['id', 'user', 'company_name', 'position', 'phone_number', 'logo', 'background_photo', 'country', 'company_size', 'country', 'city', 'specialization', 'description', 'website_url', 'is_verified']
        read_only_fields = (['id', 'user', 'is_verified'])

class PositionSerializer(serializers.ModelSerializer):
    position_title = serializers.ReadOnlyField(source='position_occupation.title')

    class Meta:
        model = Position
        fields = ['id', 'company', 'position_occupation', 'position_title', 'position_info', 'position_tools', 'position_city', 'position_country', 'position_languages', 'position_requirements', 'price_range', 'contract_type', 'photo', 'post_time']
        read_only_fields = (['company', 'post_time', 'id',])
        

class PositionMatchSerializer(serializers.Serializer):
    accepted = serializers.BooleanField(required=True)
    jobseeker_profile = serializers.IntegerField(required=False)
    position_id = serializers.IntegerField(required=True)

class PositionMatchModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Match
        fields = ['id', 'jobseeker', 'company', 'position', 'jobseeker_accepted', 'company_accepted', 'matched']

class VerificationSerializer(serializers.Serializer):
    company_id = serializers.IntegerField(required=True)
    verified = serializers.BooleanField(required=True)
