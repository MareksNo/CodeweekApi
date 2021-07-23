from django.db import models
from django.db.models import fields
from rest_framework import serializers

from .models import OccupationCategory, Occupation

class CEDOccupationCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OccupationCategory
        fields=['title']


class OccupationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Occupation
        fields = ['id', 'title', 'category']


class RetrieveOccupationCategorySerializer(serializers.ModelSerializer):
    occupations = OccupationSerializer(read_only=True, many=True)

    class Meta:
        model = OccupationCategory
        fields = ['title', 'occupations']